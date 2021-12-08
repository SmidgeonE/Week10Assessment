import numpy as np

def simulation():
    heatBuffer = 0.01
    dt = 0.1
    heatTransferCoeff = 8.7
    area = 0.13
    mass = 0.1
    specificHeatCap = 385
    initialTemp = 313.15
    envTemp = 293.15


    currentObjectTemp = np.array([initialTemp])
    DELTATemp = [currentObjectTemp - envTemp]
    timeArray = [0]
    currentTimeStep = 0
    heatTransferArray = [0]

    while DELTATemp[len(DELTATemp) - 1] > 0.01:
        heatTransferArray.append(-heatTransferCoeff * area * DELTATemp)




        currentTimeStep += 1
        timeArray.append(currentTimeStep * dt)


if __name__ == '__main__':
    simulation()
