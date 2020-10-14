import diagrams
from diagrams import Cluster, Diagram, Edge
from diagrams.generic.blank import Blank
from diagrams.onprem.network import *
from diagrams.onprem.compute import *
from diagrams.onprem.compute import *
from diagrams.onprem.database import *

with Diagram("diagram", show=True, outformat="png", direction="TB"):
    with Cluster("apigateway"):
        with Cluster("api-apigateway"):
            apiXapigateway=Nginx("mockedup-integration-api-apigateway")
    with Cluster("database"):
        with Cluster("database-database"):
            dbXdatabase=Postgresql("mockedup-integration-database-database")
    with Cluster("lambda"):
        with Cluster("api-lambda"):
            apiXlambda=Server("mockedup-integration-api-lambda")
            with Cluster("api-lambda-api"):
                apiXlambdaXapi=Server("mockedup-integration-api-lambda-api")
    apiXlambdaXapi >> Edge() << apiXapigateway
    apiXlambdaXapi >> Edge() >> dbXdatabase
