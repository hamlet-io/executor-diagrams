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

with Diagram("Graph3", show=True, outformat="png"):
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
    #format entities within one group
    oUser - Edge(color="transparent") - oDevice
    dsUser - Edge(color="transparent") - dsDevice
    ELS - Edge(color="transparent") - cognito
    msECS1 - Edge(color="transparent") - msECS2
    elasticacheForRedis - Edge(color="transparent") - mdRDS

    #connect between entities
    #default color
    elb >> Edge(style="dashed") >> maECS
    msECS1 >> Edge(style="dashed") >> ELS
    msECS1 >> Edge(style="dashed") >> elasticacheForRedis
    msECS2 >> Edge(style="dashed") >> elasticacheForRedis
    msECS2 >> Edge(style="dashed") >> simpleEmailServiceSes
    #gray dashed: System Processes
    oDevice >> Edge(style="dashed", label= "Mobile Devices retrieve updates \n of the mobile app") >> s3
    #orange: Submissions
    oDevice >> Edge(color = "#C55A11", label= "Observers submit voyage \n reports and retrieve the \n documents for their voyage") >> elb
    #green: Voyage Management
    dsDevice >> Edge(color= "#70AD47", label= "Departmental staff create \n voyages and manage their status") >> elb
    #blue: Reporting
    dsDevice >> Edge(color= "#4472C4") >> elb
    dsDevice >> Edge(color="#4472C4", label= "Departmental staff generate \n reports on voyages and \n the reports provided") >> ELS 