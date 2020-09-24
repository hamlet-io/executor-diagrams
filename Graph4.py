from diagrams import Cluster, Diagram, Edge
from diagrams.generic.device import Tablet, Mobile
from diagrams.onprem.client import Client, User

# aws resources
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.storage import S3
from diagrams.aws.general import TradicionalServer, GenericSamlToken
from diagrams.aws.engagement import SimpleEmailServiceSes
from diagrams.aws.network import ElasticLoadBalancing
from diagrams.aws.database import RDS, Elasticache
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.storage import EBS

graph_attr = {
   # "fontsize": "45",
   # "bgcolor": "transparent"
}

with Diagram("Graph4", show=True, outformat="png", graph_attr=graph_attr):

    with Cluster("Internet"):
        with Cluster("Trusted External Parties"):
            tepUser = User("")
            tepDevice = Client("")

    with Cluster("Dept"):
        with Cluster("Department Staff"):
            dsUser = User("")
            dsDevice = Client("")
        with Cluster("Department SAML SSO"):
            tradicionalServer = TradicionalServer("")
            genericSamlToken = GenericSamlToken("")

    with Cluster("AWS Cloud"):
        simpleEmailServiceSes = SimpleEmailServiceSes("Simple Email Service")

        with Cluster("Jira"):
            jELB = ElasticLoadBalancing("Load Balancer")
            jEC2 = EC2("EC2 Instance")
            jEBS = EBS("EBS Volume")
            jRDS = RDS("Relational Database Service for Postgres")

        with Cluster("Confluence"):
            cELB = ElasticLoadBalancing("Load Balancer")
            cECS = ECS("EC2 Instance")
            cEBS = EBS("EBS Volume")
            cRDS = RDS("Relational Database Service for Postgres")

    #format within Internet
    tepUser - Edge(color="transparent") - tepDevice
    #format within Dept
    dsUser - Edge(color="transparent") - dsDevice
    tradicionalServer - Edge(color="transparent") - genericSamlToken
    dsDevice >> Edge(color= "#4472C4") >> tradicionalServer
    dsDevice >> Edge(color= "#70AD47") >> genericSamlToken
    #format within Jira
    jELB >> Edge(color= "#4472C4") >> jEC2 >> Edge(color= "#4472C4", style= "dashed", label= "Issues and configuration \n stored in database") >> jRDS
    jEC2 >> Edge(color= "#4472C4", style= "dashed", label= "Jira writes attachment data \n to a dedicated data store") >> jEBS
    #format within Confluence
    cELB >> Edge(color= "#70AD47") >> cECS >> Edge(color= "#70AD47", style= "dashed", label= "Articles and configuration \n stored in database") >> cRDS
    cECS >> Edge(color= "#70AD47", style= "dashed", label= "Confluence writes attachment \n data to a dedicated data store") >> cEBS
    #connect within AWS Cloud
    jEC2 >> Edge(color= "#4472C4", style= "dashed") >> simpleEmailServiceSes 
    cECS >> Edge(color= "#70AD47", style= "dashed") >> simpleEmailServiceSes
    
    #connect between sections
    #blue: Jira Access
    #green: Confluence Access
    #blue dashed: Jira System
    #green dashed: Confluence System

    tepDevice >> Edge(color= "#4472C4", label= "Trusted Users are \n provided credentials \n from Department Staff") >> jELB
    tepDevice >> Edge(color= "#70AD47") >> cELB
    dsDevice >> Edge(color= "#4472C4") >> jELB
    dsDevice >> Edge(color= "#70AD47") >> cELB