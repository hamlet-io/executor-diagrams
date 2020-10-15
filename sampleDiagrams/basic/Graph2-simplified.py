from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet, Mobile
from diagrams.generic.blank import Blank
from diagrams.onprem.client import Client, User
# aws resources
from diagrams.aws.compute import ECS
from diagrams.aws.storage import S3
from diagrams.aws.general import TradicionalServer, GenericSamlToken
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.aws.network import ElasticLoadBalancing
from diagrams.aws.database import RDS, Elasticache


with Diagram("Graph2-simplified-test123", show=True, outformat="png", direction="TB"):
    #STEP1:set up groups and entities
    with Cluster("Public"):
        with Cluster("Client"):
            pUser = User("")
            pDevice = Client("")

    with Cluster("Dept"):
        with Cluster("Bio Security Officer"):
            bsoUser = User("")
            bsoDevice = Mobile("")

        with Cluster("Delegated Officer"):
            doUser = User("")
            doDevice = Client("")

        with Cluster("Department SAML SSO"):
            tradicionalServer = TradicionalServer("")
            genericSamlToken = GenericSamlToken("")

    with Cluster("AWS Cloud"):
        with Cluster("Management App"):
            elb = ElasticLoadBalancing("Load Balancer")
            maECS = ECS("ECS Container")

        with Cluster("Management Services"):
            msECS1 = ECS("ECS Container")
            msECS2 = ECS("ECS Container")
            simpleEmailServiceSes = SimpleEmailServiceSes("Simple Email Service")
        
        with Cluster("Mobile Updates"):
            s3 = S3("S3 Bucket")
        
        with Cluster("Management Database"):
            elasticacheForRedis = Elasticache("Elasticache for Redis")
            mdRDS = RDS("Relational Database Service for Postgres")
    


    #STEP2:set up relationships
    msECS2 >> Edge() >> simpleEmailServiceSes
    elb >> Edge() >> maECS
    pDevice >> Edge() >> elb
    bsoDevice >> Edge() >> elb
    doUser >> Edge() >> tradicionalServer
    doDevice >> Edge() >> elb 
    bsoDevice >> Edge() >> s3
    maECS >> Edge() >> elasticacheForRedis
    msECS1 >> Edge() >> elasticacheForRedis
    msECS2 >> Edge() >> elasticacheForRedis
    msECS1 >> Edge() >> pDevice 
    msECS1 >> Edge() >> bsoDevice
    msECS1 >> Edge() >> doDevice