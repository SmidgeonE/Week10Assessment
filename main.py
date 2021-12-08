import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as mpl

def simulation(isClosedSystem):
    tempBuffer = 0.01
    dt = 0.01
    heatTransferCoeff = 8.7
    interfaceArea = 0.13

    objectMass = 0.1
    objectSpecHeatCap = 385
    objectStartingTemp = 313.15

    envMass = 0.6
    envSpecHeatCap = 1000
    envStartingTemp = 293.15

    objectTemp = [objectStartingTemp]
    envTemp = [envStartingTemp]

    DELTATemp = [objectStartingTemp - envStartingTemp]
    timeArray = [0]
    currentTimeStep = 0

    timeForTempDiffToHalf = 0
    halfwayReached = False

    while DELTATemp[len(DELTATemp) - 1] > tempBuffer:
        tempChangeForObject = (-heatTransferCoeff * interfaceArea * DELTATemp[-1] * dt) / (objectMass * objectSpecHeatCap)

        objectTemp.append(objectTemp[-1] + tempChangeForObject)

        if not halfwayReached and DELTATemp[-1] < (objectStartingTemp - envStartingTemp) / 2:
            timeForTempDiffToHalf = currentTimeStep * dt
            halfwayReached = True

        if isClosedSystem:
            tempChangeForEnvironment = (heatTransferCoeff * interfaceArea * DELTATemp[-1] * dt) /\
                                       (envMass * envSpecHeatCap)
            envTemp.append(envTemp[-1] + tempChangeForEnvironment)
        else:
            envTemp.append(envStartingTemp)

        DELTATemp.append(objectTemp[-1] - envTemp[-1])
        currentTimeStep += 1
        timeArray.append(currentTimeStep * dt)

        #print()
        #print("Current temp diff : ", DELTATemp[-1])
        #print("Current temp of ball : ", objectTemp[-1])

    print("Finally, it took", timeArray[-1], "seconds (", currentTimeStep, "lots of", dt, ") to get to 0.01 of the env temp, actual difference: ", DELTATemp[-1])
    print("Final object temp:", objectTemp[-1], " Final environment temp:", envTemp[-1])
    print("Time taken to reach half of the temp difference was:", timeForTempDiffToHalf,"\n")

    mpl.plot(timeArray, objectTemp,
             timeArray, envTemp)
    mpl.vlines(timeForTempDiffToHalf, objectStartingTemp, envStartingTemp, 'black', 'dashed')
    plt.xlabel("Time /s")
    plt.ylabel("Temp /K")
    mpl.show()


if __name__ == '__main__':
    answer = input("Would you like to run the simulation as a closed system (type closed), or open (type open)?\n")
    simulation(answer.lower() == "closed")
    input()
