def registerThisClient(clientIP, clientPort):
    with open("clientlist.txt", "a") as myFile:
        myFile.write(clientIP + ":" + clientPort + "\n")
