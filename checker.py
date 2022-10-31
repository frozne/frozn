import os, requests, time, urllib3
from datetime import datetime
from termcolor import colored
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
ccFile = "cc.txt"
outputFile = "cc_checked_{}.txt".format(int(datetime.timestamp(datetime.now())))
checkerAPIURL = "https://www.xchecker.cc/api.php?cc={}|{}|{}|{}"
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    "Accept": "*/*",
}
 
def writeFileOutput(data, file, mode="a"):
    f = open(file, mode)
    f.write("{}\n".format(data))
    f.close()
    if "|Live|" in data:
        print(colored(data, "green", attrs=["bold"]))
    elif "|Dead|" in data:
        print(colored(data, "red", attrs=["bold"]))
    else:
        print(colored(data, "white", attrs=["bold"]))
 
def main():
    if os.path.exists(ccFile):
        with open(ccFile) as f:
            writeFileOutput("Running script...", outputFile)
            writeFileOutput("Output file results: {}".format(outputFile), outputFile)
            writeFileOutput("Any issue, contact me at:", outputFile)
            writeFileOutput("DISCORD: mlodykreska#0002", outputFile)
            writeFileOutput("https://github.com/Blagdoii/cc-checker", outputFile)
            writeFileOutput("----------------------------------------------", outputFile)
            for cc in f:
                cc = cc.replace("\r", "").replace("\n", "")
                try:
                    ccNumber = cc.split("|")[0]
                    expMonth = cc.split("|")[1]
                    expYear = cc.split("|")[2]
                    cvc = cc.split("|")[3]
                except:
                    writeFileOutput("{} => Format error. Use ccNumber|expMonth|expYear|cvc".format(cc), outputFile)
                    continue
                url = checkerAPIURL.format(ccNumber, expMonth, expYear, cvc)
                while True:
                    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
                    if response.status_code == 200 and "json" in response.headers["Content-Type"]:
                        data = response.json()
                        if "ccNumber" in data:
                            output = data["ccNumber"]
                            if "cvc" in data:
                                output = data["cvc"]
                            if "expMonth" in data:
                                output += "|" + data["expMonth"]
                                output += "/" + data ["expYear"]
                            output += "|" + data["status"] + "|" + data["details"]
                            output += "--->> " + data["bankName"]
                        else:
                            output = "{} => {}".format(ccNumber, data["error"])
                        writeFileOutput(output, outputFile)
                        break
                    else:
                        writeFileOutput("HTTP service error: {}, retry...".format(response.status_code), outputFile)
                        time.sleep(1000)
    else:
        print("File {} not found in current directory".format(ccFile))
 
if __name__ == "__main__":
    main()
 