from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet, Mobile
from diagrams.onprem.client import Client, User
# aws resources
from diagrams.aws.compute import ECS
from diagrams.aws.storage import S3
from diagrams.aws.general import TradicionalServer, GenericSamlToken
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.aws.network import ElasticLoadBalancing
from diagrams.aws.database import RDS, Elasticache
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.security import Cognito

with Diagram("Graph3-simplified", show=True, outformat="png"):
    #STEP1:set up groups and entities
    with Cluster("Public"):
        with Cluster("Observer"):
            oUser = User("")
            oDevice = Mobile("")

    with Cluster("Dept"):
        with Cluster("Department Staff"):
            dsUser = User("")
            dsDevice = Client("")

    with Cluster("AWS Cloud"):
        with Cluster("Mobile Updates"):
            s3 = S3("S3 Bucket")

        with Cluster("Management App"):
            elb = ElasticLoadBalancing("Load Balancer")
            maECS = ECS("ECS Container")

        with Cluster("Search and Reporting"):
            ELS = ElasticsearchService("ElasticSearch")
            cognito = Cognito("Cognito")

        with Cluster("Management Services"):
            msECS1 = ECS("ECS Container")
            msECS2 = ECS("ECS Container")
            simpleEmailServiceSes = SimpleEmailServiceSes("Simple Email Service")

        with Cluster("Management Database"):
            elasticacheForRedis = Elasticache("Elasticache for Redis")
            mdRDS = RDS("Relational Database Service for Postgres")

    #STEP2:set up relationships
    elb >> Edge() >> maECS
    msECS1 >> Edge() >> ELS
    msECS1 >> Edge() >> elasticacheForRedis
    msECS2 >> Edge() >> elasticacheForRedis
    msECS2 >> Edge() >> simpleEmailServiceSes
    oDevice >> Edge() >> s3
    oDevice >> Edge() >> elb
    dsDevice >> Edge() >> elb
    dsDevice >> Edge() >> elb
    dsDevice >> Edge() >> ELS 