from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet, Mobile
from diagrams.onprem.client import Client, User

# aws resources
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.storage import S3
from diagrams.aws.general import TradicionalServer, GenericSamlToken
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.aws.network import ElasticLoadBalancing
from diagrams.aws.database import RDS, Elasticache
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.security import Cognito
from diagrams.aws.mobile import APIGateway
from diagrams.aws.integration import SQS

with Diagram("Graph5", show=True, outformat="png"):

    with Cluster("Public and Rangers"):
        with Cluster("Public"):
            pUser = User("")
            pDevice = Client("")
        with Cluster("Rangers"):
            rUser = User("")
            rDevice = Mobile("")

    with Cluster("Dept"):
        with Cluster("Department Staff"):
            dsUser = User("")
            dsDevice = Client("")
        with Cluster("Department SAML SSO"):
            tradicionalServer = TradicionalServer("")
            genericSamlToken = GenericSamlToken("")

    with Cluster("AWS Cloud"):  

        with Cluster("Community Engagement Web App"):
            cewpELB = ElasticLoadBalancing("Load Balancer")
            cewaECS = ECS("ECS Container")

        with Cluster("Open311 API"):
            api = APIGateway("API Gateway")
            lambda1 = Lambda("Lambda Function")

        with Cluster("Management App | Configuration API"):
            macaELB = ElasticLoadBalancing("Load Balancer")
            macaECS = ECS("ECS Container")
        

        with Cluster("Open311 Data Store"):
            s3a = S3("S3 Bucket")
            s3b = S3("S3 Bucket")
            s3c = S3("S3 Bucket")
            s3d = S3("S3 Bucket")
            sqs = SQS("SQS Queue")

        with Cluster("Integration Process | Management App"):
            ipmaECS1 = ECS("ECS Container")
            ipmaECS2 = ECS("ECS Container")
            ses = SimpleEmailServiceSes("Simple Email Service")

        with Cluster("Management Database"):
            elasticacheForRedis = Elasticache("Elasticache for Redis")
            mdRDS = RDS("Relational Database Service for Postgres")



    #format within Public and Rangers
    pUser - Edge(color="transparent") - pDevice
    rUser - Edge(color="transparent") - rDevice
    #format within Dept
    dsUser - Edge(color="transparent") - dsDevice
    tradicionalServer - Edge(color="transparent") - genericSamlToken
    
    #format within Community Engagement Web App
    cewpELB - Edge(color="transparent") - cewaECS
    #format within Open311 API
    api - Edge(color="transparent") - lambda1
    #format within Management App | Configuration API
    macaELB - Edge(color="transparent") - macaECS
    
    #format within Open311 Data Store
    s3a - Edge(color="transparent") - s3b
    s3c - Edge(color="transparent") - s3d
    #format within Integration Process | Management App
    ipmaECS1 - Edge(color="transparent") - ipmaECS2

    #connect between sections
    #orange
    pDevice >> Edge(color = "#C55A11", label= "Ranger or a member of the \n public submits a report") >> cewpELB
    rDevice >> Edge(color = "#C55A11", label= "Ranger App Authenticates \n Retrieves Report Requests") >> api
    cewaECS >> Edge(color = "#C55A11", label= "Community Engagement web app \n submits report to Open311 API") >> api
    lambda1 >> Edge(color = "#C55A11", label= "API saves the \n report in the data store") >> s3d

    #blue
    rDevice >> Edge(color = "#00B0F0") >> macaELB
    dsDevice >> Edge(color = "#00B0F0", label= "Staff Submit \n Report Requests") >> macaELB

    #dark blue
    ipmaECS2 >> Edge(color = "#4472C4", label= "Integration processing retrieves \n open311 reports from the datastore") >> sqs
    ipmaECS2 >> Edge(color = "#4472C4", label= "integration validates data \n and saves to database") >> mdRDS

    #yellow
    genericSamlToken >> Edge(color = "#FFC000") >> macaELB
    macaELB >> Edge(color = "#FFC000", label= "Feedback sent to user via email") >> ses

    #green #70AD47
    dsDevice >> Edge(color = "#70AD47", label= "Staff Assess Submitted reports \n Staff Provide Feedback") >> macaELB

    #double arrows
    genericSamlToken >> Edge(color = "#00B0F0") << macaELB
    genericSamlToken >> Edge(color = "#70AD47", label= "Departmental Staff Authenticate") << macaELB
    genericSamlToken >> Edge(color = "#FFC000") << macaELB
    
    macaECS >> Edge(color = "#00B0F0") << mdRDS
    macaECS >> Edge(color = "#70AD47") << mdRDS
    macaECS >> Edge(color = "#FFC000", label= "Report updates saved to database") << mdRDS