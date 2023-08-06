import anteater
import sys


if __name__ == '__main__':
    print("welcome")
    """anteater.help()
    anteater = anteater.Anteater(testFile="./src/test.txt", similarFunc=1, k_mer=4, viewModel=1).run()"""
    testFile = sys.argv[1]
    similarFunc = int(sys.argv[2])
    k_mer = int(sys.argv[3])
    viewModel = sys.argv[4]
    anteater = anteater.Anteater(testFile, similarFunc, k_mer, viewModel)
    anteater.run()