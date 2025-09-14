from src.tamer.sac.sacBuild import env
from src.tamer.sac.sacPredict import sac_agent, evaluate, run_PSAC_TAMER

if __name__ == '__main__':
    run_PSAC_TAMER()
   # sac_model = sac_agent()
   # rewards = evaluate(env, sac_model.actor, "")
   # print("averageReward:", sum(rewards) / len(rewards))


