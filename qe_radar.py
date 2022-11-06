import requests

QEC = "1.0" #Version number for challenge, can check with site for compatability,
# will provide appropriate error message when different to server to help communicate with teams that urgent updates are needed

class DevSimulator (object):

    token = ""

    def __init__(self, token: str = ""):
        self.token = token
        self.URL = "https://sim.quantumnextgen.com.au/dev/"

    def authentication(self, token: str):
        """Updates the access token used by the simulator connector"""
        self.token = token

    def simulate(self, pulse: list[int], measure: list, example: int) -> float:
        """
        Runs the provided configuration into the simulator and returns a normalised signal as a float
        
        Keyword arguments:
        pulse -- paired list with start and end of pulse in us (0-500,000)
        measure -- list with start and end of the measurement window in us (0-500 000) and phase in radians
        example -- id of example chosen for the simulation (0-999)
        """
        #creates JSON form data for HTTP request
        payload = {"pulse":pulse, "measurement":measure}
        
        #sends data to site, stores in variable r
        r = self.post(payload, str(example))
        data = r.json
        if r.status_code != 200:
            raise Exception(r.text)
        else:
            #return to user the actual value of the request, removing header and online data that is unneeded
            return float(r.text)

    #Directly calls dev_data() in qe_radar
    def dataset(self, example) -> list:
        """Requests the Rabi, Detuning, and Time of Flight for the chosen example target."""

        #sends data to site, stores in variable r
        r = self.get(str(example))
        data = r.json()

        if r.status_code != 200:
            raise Exception(r.text)
        else:
            #return to user the actual value of the request, removing header and online data that is unneeded
            return [data['Rabi'], data['Detuning'], data['T_Flight']]

    def validate_config(self, configs: list) -> bool:
        
        payload = {"configuration":configs}

        r = self.post(payload, "config")
        data = r.json()

        if r.status_code != 200:
            raise Exception(r.text)
        else:
            if data['Valid'] == True:
                print('Configurations are Valid')
                return True
            else:
                for i in data['Error']:
                    print(i)
                return False

    def validate_estimate(self, estimates: list) -> bool:
        
        payload = {"estimates":estimates}

        r = self.post(payload, "estimates")
        data = r.json()

        if r.status_code != 200:
            raise Exception(r.text)
        else:
            if data['Valid'] == True:
                print('Estimates are Valid')
                return True
            else:
                for i in data['Error']:
                    print(i)
                return False

    def post(self, payload, ref=""):
        return requests.post(self.URL+ref, json=payload, headers={'Authentication': self.token, 'QeC':QEC})

    def get(self, ref=""):
        return requests.get(self.URL+ref, headers={'Authentication': self.token, 'QeC':QEC})

class TestSimulator(object):
    def __init__(self, token: str = "") -> None:
        self.token = token
        self.URL = "https://sim.quantumnextgen.com.au/test/"

    def authentication(self, token: str):
        self.token = token

    def simulate(self, pulse: list[int], measure:list, example:int):
        #creates JSON form data for HTTP request
        payload = {"pulse":pulse, "measurement":measure}

        #sends data to site, stores in variable r
        r = self.post(payload)
        data = r.json

        if r.status_code != 200:
            raise Exception(r.text)
        #return to user the actual value of the request, removing header and online data that is unneeded
        else:
            return float(r.text)

    def score(self, configs:list, estimates:int):
        payload = {"configurations":configs, "estimates":estimates}
        r = self.post(payload, "score")
        data = r.json
        if r.status_code != 200:
            raise Exception(r.text)
        else:
            if data['Valid'] == True:
                return [data['Score'], [data['Rabi_Std'],data['Detuning_Std'],data['T_Flight_Std']],[data['Rabi_Mean'],data['Detuning_Mean'],data['T_Flight_Mean']]]
            else:
                for i in data['Error']:
                    print(i)
                return None

    def post(self, payload, ref=""):
        return requests.post(self.URL+ref, json=payload, headers={'Authentication': self.token, 'QeC':QEC})

    def get(self, ref=""):
        return requests.get(self.URL+ref, headers={'Authentication': self.token, 'QeC':QEC})