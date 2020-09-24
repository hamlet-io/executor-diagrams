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

with Diagram("Graph2", show=True, outformat="png"):

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
            #bl = Blank(" ")
            mdRDS = RDS("Relational Database Service for Postgres")
    
    #format within Public section
    pUser - Edge(color="transparent") - pDevice
    #format within Dept section
    bsoUser - Edge(color="transparent") - bsoDevice
    doUser - Edge(color="transparent") - doDevice
    tradicionalServer - Edge(color="transparent") - genericSamlToken
    #format within Management App
    elb >> Edge(style="dashed") >> maECS
    #format within Management Services
    msECS1 - Edge(color="transparent") - msECS2
    msECS2 >> Edge(style="dashed") >> simpleEmailServiceSes
    #format within Management Database
    elasticacheForRedis - Edge(color="transparent") - mdRDS
    msECS2 >> Edge(style="dashed", label= "Feed provided to all \n users using email ") >> simpleEmailServiceSes
    
    #connect between sections
    #yellow: Feedback
    
    #orange: Submission
    pDevice >> Edge(color = "#C55A11", label= "Client Submits a \n Permit Application") >> elb
    #green: Inspection
    bsoDevice >> Edge(color= "#70AD47", label= "BioSecurity Officer Conduct \n the inspection and \n submits the results") >> elb
    #blue: Assessment
    doUser >> Edge(color="#4472C4", label= "Delegated Officer uses \n departmental SSO to \n access system") >> tradicionalServer
    doDevice >> Edge(color="#4472C4", label= "Delegated Officer Assesses \n the application and \n inspection results") >> elb 
    #gray dashed: System Processes
    bsoDevice >> Edge(style="dashed", label= "BioSecurity Officer mobile \n app retrieves latest application \n version from the update store") >> s3

    maECS >> Edge(style="dashed") >> elasticacheForRedis
    msECS1 >> Edge(style="dashed") >> elasticacheForRedis
    msECS2 >> Edge(style="dashed") >> elasticacheForRedis
    
    msECS1 >> Edge(color = "#FFC000") >> pDevice 
    msECS1 >> Edge(color = "#FFC000") >> bsoDevice
    msECS1 >> Edge(color = "#FFC000") >> doDevice