from kafkaLogic.consumeTrainAndProduce import consumeTrainAndProduce
from kafkaLogic.read_config import read_config


def main():
  config = read_config()
  consumeTrainAndProduce(config)


if __name__ == "__main__":
    main()