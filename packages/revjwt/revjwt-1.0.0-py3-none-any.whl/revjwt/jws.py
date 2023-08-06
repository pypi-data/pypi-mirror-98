import json
from typing import Any, Dict, List

import requests
from jwcrypto.jwk import JWK
from jwt.api_jws import PyJWS
from jwt.exceptions import DecodeError

from revjwt.algorithms import KMSAlgorithm


class JWS(PyJWS):
    def __init__(self, options: Any = None) -> None:
        super().__init__(options)  # type: ignore
        self._algorithms = {"RS256": KMSAlgorithm()}

    def decode_complete(
        self,
        jwt: str,
        key: str = "",
        algorithms: List[str] = ["RS256"],
        options: Any = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        if options is None:
            options = {}
        merged_options = {**self.options, **options}
        verify_signature = merged_options["verify_signature"]

        if verify_signature and not algorithms:
            raise DecodeError(
                'It is required that you pass in a value for the "algorithms" argument when calling decode().'
            )

        payload, signing_input, header, signature = self._load(jwt)  # type: ignore

        json_payload = json.loads(payload.decode())
        try:
            host, version = json_payload["iss"].split("/")
        except ValueError:
            host, version = None, "v1"
        kid = header["kid"]

        env = json_payload.get("env", None)

        if not env and host:
            env = host.split(".")[0][-4:]

            if env in ["-stg", "-dev"]:
                host = "https://auth-stg.revtel-api.com"
            else:
                host = "https://auth.revtel-api.com"

        if version not in ["v2", "v1"]:
            url = f"{host}/{version}/certs"
            resp = requests.get(url).json()["keys"]
            key = [key for key in resp if key["kid"] == kid][0]
        else:
            resp = requests.get("https://keys.revtel-api.com/pub.json").json()
            key = [key for key in resp if key["kid"] == kid][0]

        key_json = JWK.from_json(json.dumps(key))
        key_pem = key_json.export_to_pem()

        if verify_signature:
            self._verify_signature(signing_input, header, signature, key_pem, algorithms)  # type: ignore

        return {
            "payload": payload,
            "header": header,
            "signature": signature,
        }


_jws = JWS()
encode = _jws.encode
decode = _jws.decode_complete
