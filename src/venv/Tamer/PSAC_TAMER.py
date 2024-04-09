# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import torch.nn.functional as F
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
import numpy as np
import gym
from matplotlib import pyplot as plt
import os
import PSAC_LOSSFUNC 
import userOutFeedback
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
env = gym.make("Pendulum-v0").unwrapped
'''Pendulum'''
state_number=env.observation_space.shape[0]
action_number=env.action_space.shape[0]
max_action = env.action_space.high[0]
min_action = env.action_space.low[0]
RENDER=False
EP_MAX = 500
EP_LEN = 500
GAMMA = 0.9
q_lr = 2e-3
value_lr = 3e-3
policy_lr = 1e-3
BATCH = 128
tau = 1e-2
MemoryCapacity=10000
Switch=0

class ActorNet(nn.Module):
    def __init__(self,inp,outp):
        super(ActorNet, self).__init__()
        self.in_to_y1=nn.Linear(inp,256)
        self.in_to_y1.weight.data.normal_(0,0.1)
        self.y1_to_y2=nn.Linear(256,256)
        self.y1_to_y2.weight.data.normal_(0,0.1)
        self.out=nn.Linear(256,outp)
        self.out.weight.data.normal_(0,0.1)
        self.std_out = nn.Linear(256, outp)
        self.std_out.weight.data.normal_(0, 0.1)

    def forward(self,inputstate):
        inputstate=self.in_to_y1(inputstate)
        inputstate=F.relu(inputstate)
        inputstate=self.y1_to_y2(inputstate)
        inputstate=F.relu(inputstate)
        mean=max_action*torch.tanh(self.out(inputstate))#
        log_std=self.std_out(inputstate)#softplus
        log_std=torch.clamp(log_std,-20,2)
        std=log_std.exp()
        return mean,std

class CriticNet(nn.Module):
    def __init__(self,input):
        super(CriticNet, self).__init__()
        self.in_to_y1=nn.Linear(input,256)
        self.in_to_y1.weight.data.normal_(0,0.1)
        self.y1_to_y2=nn.Linear(256,256)
        self.y1_to_y2.weight.data.normal_(0,0.1)
        self.out=nn.Linear(256,1)
        self.out.weight.data.normal_(0,0.1)
    def forward(self,inputstate):
        v=self.in_to_y1(inputstate)
        v=F.relu(v)
        v=self.y1_to_y2(v)
        v=F.relu(v)
        v=self.out(v)
        return v
class QNet(nn.Module):
    def __init__(self,input,output):
        super(QNet, self).__init__()
        self.in_to_y1=nn.Linear(input+output,256)
        self.in_to_y1.weight.data.normal_(0,0.1)
        self.y1_to_y2=nn.Linear(256,256)
        self.y1_to_y2.weight.data.normal_(0,0.1)
        self.out=nn.Linear(256,output)
        self.out.weight.data.normal_(0,0.1)
    def forward(self,s,a):
        inputstate = torch.cat((s, a), dim=1)
        q1=self.in_to_y1(inputstate)
        q1=F.relu(q1)
        q1=self.y1_to_y2(q1)
        q1=F.relu(q1)
        q1=self.out(q1)
        return q1
class Memory():
    def __init__(self,capacity,dims):
        self.capacity=capacity
        self.mem=np.zeros((capacity,dims))
        self.memory_counter=0
    '''memory in pool'''
    def store_transition(self,s,a,r,s_):
        tran = np.hstack((s, [a.squeeze(0),r], s_))  #
        index = self.memory_counter % self.capacity#
        self.mem[index, :] = tran  # 
        self.memory_counter+=1
    '''radom get from memory'''
    def sample(self,n):
        assert self.memory_counter>=self.capacity,'not full in memory'
        sample_index = np.random.choice(self.capacity, n)#
        new_mem = self.mem[sample_index, :]#
        return new_mem
class Actor():
    def __init__(self):
        self.action_net=ActorNet(state_number,action_number)#这只是均值mean
        self.optimizer=torch.optim.Adam(self.action_net.parameters(),lr=policy_lr)

    def choose_action(self,s):
        inputstate = torch.FloatTensor(s)
        mean,std=self.action_net(inputstate)
        dist = torch.distributions.Normal(mean, std)
        action=dist.sample()
        action=torch.clamp(action,min_action,max_action)
        return action.detach().numpy()
    #add NonTaskReply
    def choose_actionU(self,s,list,_nonReplySet):
        action=choose_action(s)
        action=getWholeAction(action,list,_nonReplySet)
        return action.detach().numpy() 
    def evaluate(self,s):
        inputstate = torch.FloatTensor(s)
        mean,std=self.action_net(inputstate)
        dist = torch.distributions.Normal(mean, std)
        noise = torch.distributions.Normal(0, 1)
        z = noise.sample()
        action=torch.tanh(mean+std*z)
        action=torch.clamp(action,min_action,max_action)
        action_logprob=dist.log_prob(mean+std*z)-torch.log(1-action.pow(2)+1e-6)
        return action,action_logprob,z,mean,std

    def learn(self,actor_loss):
        loss=actor_loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

class Critic():
    def __init__(self):
        self.critic_v,self.target_critic_v=CriticNet(state_number),CriticNet(state_number)#
        self.optimizer = torch.optim.Adam(self.critic_v.parameters(), lr=value_lr,eps=1e-5)
        self.lossfunc = nn.MSELoss()
    def soft_update(self):
        for target_param, param in zip(self.target_critic_v.parameters(), self.critic_v.parameters()):
            target_param.data.copy_(target_param.data * (1.0 - tau) + param.data * tau)

    def get_v(self,s):
        return self.critic_v(s)

    def learn(self,expected_v,next_v):
        loss=self.lossfunc(expected_v,next_v.detach())
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

class Q_Critic():
    def __init__(self):
        self.q1_net=QNet(state_number,action_number)#
        self.q1_optimizer = torch.optim.Adam(self.q1_net.parameters(), lr=q_lr,eps=1e-5)
        self.lossfunc = nn.MSELoss()
    def get_q(self,s,a):
        return self.q1_net(s,a)
    def learn(self,br,expected_q,target_v):
        next_q = br + GAMMA * target_v
        loss=self.lossfunc(expected_q,next_q.detach())
        self.q1_optimizer.zero_grad()
        loss.backward()
        self.q1_optimizer.step()
class MOC_Policy():
    def __init__(self,replySetsNum,lowTaskAnswer,upperTaskAnswer,lowNonTaskReplyset,upperNonTaskReplyset):
        self.replySetsNum=replySetsNum
        self.lowTaskAnswer=lowTaskAnswer
        self.upperTaskAnswer=upperTaskAnswer
        self.lowNonTaskReplyset=lowNonTaskReplyset
        self.upperNonTaskReplyset=upperNonTaskReplyset
        self.replySets_counter=0
    def _generateTaskAnswers(self,density):
        if density>=self.upperTaskAnswer :
         self.replySets_counter=1
         return True
        else :
         return False
    def _judgeNonTaskAnswers(self,densityTaskAnswer):
        if densityTaskAnswer<self.lowTaskAnswer or  self.replySetsNum>1 :
         return False
    def _discardNonTaskAnswers(self,densityNonTAOne): 
        if densityNonTAOne< self.lowNonTaskReplyset :
         return True
        else :
         return False
    def _generateNonTaskAnswers(self,densityNonTAOne): 
        if densityNonTAOne>=self.UppNonTaskReplyset:
         self.replySets_counter+=1
         return True
        else :
         return False
class TAMER(): 
    def __init__(self):
        self.discountTextLength='FKscore/10'
        self.discountText=0.784
        self.lossfunc = PSAC_LOSSFUNC.calculate_sse()
    def _getRealText(oldText):
        textNumer,_TextList=gettextfromMysql(oldText);#gettextOrderNofromMysql,namely,calculate the whole text length from the start of conversation 
        text_all_Len=0;
        if oldText>0:
          for text in _TextList:
          text_all_Len+= textNumer*self.discountText
        return text_all_Len
    def _getIQAssessment(self,oldText,answerText,user,dim,feature_Data):
        #get Interative Evalution
        #out Interface outcome  from viewer
        tag=feature_Data.predictTag;  #get oberverFeatureTag 
        sen_add=getCurrentLatestText(oldText)
        res=userOutFeedback._get_user_feedback(sen_add,tag,answerText,user,dim)
        print("user:"+user+";dim:"+dim+";socre:"+res)
    def _getIQAverage(self,oldText,answerText,userLists,feature_Data):
        IQ_All=0;
        dim_list = ['coherence', 'usefulness','proactivity']
        for user in userLists:
           for dim in dim_list:
             IQ_All+=_getIQAssessment(oldText,answerText,user,dim,feature_Data)
        IQ_All=IQ_All/len(userLists)
        return IQ_All
    def _getUserSatisfaction(self,IQScore):
        if IQScore < 4 :
          return 0
        else :
          return 1
    def _getRewadRaw(oldText,answerText,userLists):
       IQScore=_getIQAverage(oldText,answerText,userLists)
       rewardValue = _getRealText(oldText)*(-1)+_getUserSatisfaction(IQScore)*20
       return rewardValue
    def learn(self,oldText,answerText,userLists,next_v,feature_Data):
        expect_reward=_getRewadRaw(oldText,answerText,userLists)
        loss=self.lossfunc(expect_reward,next_v.detach(),feature_Data)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
if Switch==0:
    print('SAC training...')
    #get date form Mysql
    diaglgue_Data=[]
    userLists=getUserInfoList();
    answerText="";
    #get oberverFeature from  BiLSTMCRF
    feature_Data=BiLSTM.getFeatureVec(diaglgue_Data);
    Observer_,Prediction_=BiLSTM.getCRFPrediction(feature_Data);
    actor = Actor()
    critic = Critic()
    q_critic=Q_Critic()
    reply_sets_num=0;
    M = Memory(MemoryCapacity, 2 * state_number + action_number + 1)
    all_ep_r = []
    for episode in range(EP_MAX):
        observation = env.reset()  # 
        reward_totle = 0
        for timestep in range(EP_LEN):
            if RENDER:
                env.render()
            #get action
            taskAnswer_Prediction=Prediction_.taskAnswer_Pre
            #get TaskAnswerAction
            if MOC_Policy._generateTaskAnswers():
               action = actor.choose_action(observation)
               reply_sets_num+=1
            while 1=1:
              replyAnswerFlag=False
              _nonReplySet=[];
              if not MOC_Policy._judgeNonTaskAnswers(Prediction_.taskAnswer_Pre):
                NonTaskDialogueList[]=getNonTaskDialogueList(Prediction_)
                for a in NonTaskDialogueList:
                  if MOC_Policy._discardNonTaskAnswers(a.densityNonTA) :
                    continue;
                  if MOC_Policy._generateNonTaskAnswers(a.densityNonTA) :
                    reply_sets_num+=1
                    _nonReplySet.append(a.NonTAaction)
                  if reply_sets_num> MOC_Policy.replySetsNum :
                   replyAnswerFlag=True;
                   break;
                else :
                  break;
                if replyAnswerFlag :
                  action = actor.choose_actionU(observation,NonTaskDialogueList,_nonReplySet)
                  break;
                #update observation
            observation_, reward, done, info = env.step(action)  
            # add  Tamer FeedBack
            reward=tamer.learn(diaglgue_Data,answerText,userLists,reward,feature_Data)
            M.store_transition(observation, action, reward, observation_)
            # store in pool
            if M.memory_counter > MemoryCapacity:
                b_M = M.sample(BATCH)
                b_s = b_M[:, :state_number]
                b_a = b_M[:, state_number: state_number + action_number]
                b_r = b_M[:, -state_number - 1: -state_number]
                b_s_ = b_M[:, -state_number:]
                b_s = torch.FloatTensor(b_s)
                b_a = torch.FloatTensor(b_a)
                b_r = torch.FloatTensor(b_r)
                b_s_ = torch.FloatTensor(b_s_)
                expected_q=q_critic.get_q(b_s,b_a)
                expected_v=critic.get_v(b_s)
                new_action, log_prob, z, mean, log_std = actor.evaluate(b_s)
                target_v=critic.target_critic_v(b_s_)
                q_critic.learn(b_r,expected_q,target_v)
                expected_new_q=q_critic.get_q(b_s,new_action)
                next_v=expected_new_q-log_prob
                critic.learn(expected_v,next_v)
                log_prob_target=expected_new_q-expected_v
                actor_loss=(log_prob*(log_prob-log_prob_target).detach()).mean()
                mean_loss=1e-3*mean.pow(2).mean()
                std_loss=1e-3*log_std.pow(2).mean()
                actor_loss+=mean_loss+std_loss
                actor.learn(actor_loss)
                # soft update
                critic.soft_update()
            observation = observation_
            reward_totle += reward
        print("Ep: {} rewards: {}".format(episode, reward_totle))
        # if reward_totle > -10: RENDER = True
        all_ep_r.append(reward_totle)
        if episode % 20 == 0 and episode > 200:
            save_data = {'net': actor.action_net.state_dict(), 'opt': actor.optimizer.state_dict(), 'i': episode}
            torch.save(save_data, "E:\model_SAC.pth")
    env.close()
    plt.plot(np.arange(len(all_ep_r)), all_ep_r)
    plt.xlabel('Episode')
    plt.ylabel('Moving averaged episode reward')
    plt.show()
else:
    print('SAC testing ...')
    aa=Actor()
    checkpoint_aa = torch.load("D:\model_SACBench.pth")
    aa.action_net.load_state_dict(checkpoint_aa['net'])
    for j in range(10):
        state = env.reset()
        total_rewards = 0
        for timestep in range(EP_LEN):
            env.render()
            action = aa.choose_action(state)
            new_state, reward, done, info = env.step(action) 
            total_rewards += reward
            state = new_state
        print("Score：", total_rewards)
    env.close()