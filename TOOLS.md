#### Setup MongoDB

`helm repo add bitnami https://charts.bitnami.com/bitnami`

`helm repo update`

`helm install mongo-release --set auth.rootPassword=password1,auth.username=root,auth.password=password1,auth.database=example-mongodb bitnami/mongodb`


