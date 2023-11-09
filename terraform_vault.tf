export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=XXXXXXXXXXXXX

provider "vault" {
    # address defaults to $VAULT_ADDR
    # token defaults to $VAULT_TOKEN
}

data "vault_generic_secret" "aws_creds" {
    path = "secret/aws"
}

provider "aws" {
  region  = data.vault_generic_secret.aws_creds.data["region"]
    access_key = data.vault_generic_secret.aws_creds.data["aws_access_key_id"]
    secret_key = data.vault_generic_secret.aws_creds.data["aws_secret_access_key"]
}
