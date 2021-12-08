import matplotlib.pyplot as plt

def simulation(isClosedSystem: bool):
    # These define the constants in this simulation
    tempBuffer = 0.01
    dt = 1
    heatTransferCoeff = 8.7
    interfaceArea = 0.13

    # These are the constants related only to the object
    objectMass = 0.1
    objectSpecHeatCap = 385
    objectStartingTemp = 313.15

    # These are the constants related to the environment, ignored if it is an open system
    envMass = 0.6
    envSpecHeatCap = 1000
    envStartingTemp = 293.15

    # These are used to store data about the temps at different dts
    # envTemp simply just has envStartingTemp in it for open systems for all dt
    objectTemp = [objectStartingTemp]
    envTemp = [envStartingTemp]

    # These hold unrelated to the object or the environment that are updated for all dt
    DELTATemp = [objectStartingTemp - envStartingTemp]
    timeArray = [0]
    currentTimeStep = 0

    # These record the half-way point for the temp difference.
    timeForTempDiffToHalf = 0
    halfwayReached = False

    # Iterates until the difference between the temps is smaller that 0.01K
    while DELTATemp[len(DELTATemp) - 1] > tempBuffer:
        # We can say that the temp Change for an object, delt = Q_therm(t)/(mc)
        # We know that Q_heat(t) = -hA*(DELT) [DELT = temp diff between objects]
        # If we assume Q_therm(t) = Q_heat(t) [so no changes of state, etc.], then:
        # delt = -hA*(DELT)/(mc).
        tempChangeForObject = (-heatTransferCoeff * interfaceArea * DELTATemp[-1] * dt) / (objectMass * objectSpecHeatCap)

        # Applies temp change to object, records it to array
        objectTemp.append(objectTemp[-1] + tempChangeForObject)

        # Records the first time value when the temp difference is half the start value
        if not halfwayReached and DELTATemp[-1] < (objectStartingTemp - envStartingTemp) / 2:
            timeForTempDiffToHalf = currentTimeStep * dt
            halfwayReached = True

        # If the user said closed system, it will apply temp change to environment
        # If not, it will just keep the environment temp the same
        if isClosedSystem:
            tempChangeForEnvironment = (heatTransferCoeff * interfaceArea * DELTATemp[-1] * dt) /\
                                       (envMass * envSpecHeatCap)
            envTemp.append(envTemp[-1] + tempChangeForEnvironment)
        else:
            envTemp.append(envStartingTemp)

        # Records new temp difference, and iterates time.
        DELTATemp.append(objectTemp[-1] - envTemp[-1])
        currentTimeStep += 1
        timeArray.append(currentTimeStep * dt)

        # Debug commands
        #print()
        #print("Current temp diff : ", DELTATemp[-1])
        #print("Current temp of ball : ", objectTemp[-1])

    print("\nFinally, it took", timeArray[-1], "seconds (", currentTimeStep, "lots of", dt, ") to get to 0.01 of the env temp, actual difference: ", DELTATemp[-1])
    print("Final object temp:", objectTemp[-1], " Final environment temp:", envTemp[-1])
    print("Time taken to reach half of the temp difference was:", timeForTempDiffToHalf,"\n")

    # Plotting the outcome of the simulation
    plt.plot(timeArray, objectTemp, 'purple', label='Object Temp')
    plt.plot(timeArray, envTemp, 'pink', label='Environment Temp')
    plt.vlines(timeForTempDiffToHalf, objectStartingTemp, envStartingTemp, 'black', 'dashed', 'Half Temp')
    plt.xlabel("Time /s")
    plt.ylabel("Temp /K")
    plt.title('Cooling Object Temp against Time')
    plt.legend()
    plt.show()
    print("Plot Created Successfully")

    # Returning the 3 sets of data: Temp of object, Temp of Environment, and the Temp difference
    return objectTemp, envTemp, DELTATemp


if __name__ == '__main__':

    answer = input("Would you like to run the simulation as a closed system (type closed), or open (type open)?\n")
    objectTemp, envTemp, DELTATemp = simulation(answer.lower() == "closed")

    if input("\nWould you like to see the data? (Y/N)\n") == 'Y':
        print("Temperatures of objects :", objectTemp, "\n")
        print("Temperatures of environment :", envTemp, "\n")
        print("Temperatures difference :", DELTATemp, "\n")
    else:
        print("\nThank you")
        input()
