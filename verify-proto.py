import requests

class Verifier:
    
    def __init__(
        self,
        source: str,
        contract_name: str,
        contract_address: str, 
        verifier_api_key: str,
        license_type: str,
        constructor_args = [],
        source_format: str = 'json',
        compiler_version: str = "",
        optimizer_runs: int = 0,
        evm_version: str = "london",
        chain_id: int = 1
        ):
        self.source = source
        self.contract_name = contract_name 
        self.contract_address = contract_address
        self.verifier_api_key = verifier_api_key
        self.license_type = license_type
        self.constructor_args = constructor_args
        self.source_format = source_format
        self.compiler_version = compiler_version
        self.optimizer_runs = optimizer_runs
        self.evm_version = evm_version
        self.chain_id = chain_id

    def _base_verifier_request(self, url, payload, headers=None):
        """
        Base function to handle the POST requests for verification.
        """
        if headers is None:
            headers = {"Content-Type": "multipart/form-data"}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    def etherscan_verifier(self):
        """
        Etherscan verification.
        """
        print('Verifying on Etherscan...')
        url = f"https://api.etherscan.io/api?module=contract&action=verifysourcecode&apikey={self.verifier_api_key}"
        payload = {
            "chainId": self.chain_id,
            "codeformat": 'solidity-standard-json-input' if self.source_format == 'json' else 'solidity-single-file',
            "sourceCode": self.source,
            "contractaddress": self.contract_address,
            "contractname": self.contract_name,
            "compilerversion": self.compiler_version, 
            "constructorArguements": self.constructor_args
        }
        return self._base_verifier_request(url, payload)

    def blockscout_verifier(self):
        """
        Blockscout verification.
        """
        print('Verifying on Blockscout...')
        chainscout_chains = requests.get("https://raw.githubusercontent.com/blockscout/chainscout/main/data/chains.json")
        verifier_endpoint = f"{chainscout_chains.json()[self.chain_id]['explorers'][0]['url']}/api/v2/smart-contracts/{self.contract_address}/verification/via/"
        
        optimized = False if self.optimizer_runs == 0 else True
        url = verifier_endpoint + "flattened-code" if self.source_format == "flattened" else verifier_endpoint + self.source_format
        
        payload = {
            "compiler_version": self.compiler_version,
            "license_type": self.license_type,
            "source_code": self.source,
            "is_optimization_enabled": optimized,
            "optimization_runs": self.optimizer_runs,
            "contract_name": self.contract_name,
            "evm_version": self.evm_version,
            "autodetect_constructor_args": True,
            # Add libraries if needed
        }
        return self._base_verifier_request(url, payload)

    def sourcify_verifier(self):
        """
        Sourcify verification.
        """
        print('Verifying on Sourcify...')
        # Placeholder for Sourcify verification logic
        pass

    def verify(self, verifier: str = 'etherscan'):
        """
        Main verification method that calls the appropriate verifier.
        """
        verifiers = {
            "etherscan": self.etherscan_verifier,
            "blockscout": self.blockscout_verifier,
            "sourcify": self.sourcify_verifier
        }
        if verifier in verifiers:
            return verifiers[verifier]()
        else:
            raise ValueError(f"Unsupported verifier: {verifier}")
