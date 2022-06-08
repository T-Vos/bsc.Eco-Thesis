from downloadFunctions.moralis import Moralis

def downloadChunker(blockstart = 13315175,blocks_step = 1000):
    for i in range(0,5):
        print("Itteration:" + str(i))
        blockStep = (i*blocks_step)+blockstart
        Moralis(blocks=blocks_step, block_start=blockStep,data_folder="./data/Moralis/")
        print("downloaded until:" + str(blockStep -1))