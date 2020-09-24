from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client, User

# aws resources
from diagrams.aws.compute import Lambda
from diagrams.aws.network import CloudFront
from diagrams.aws.mobile import APIGateway
from diagrams.aws.storage import S3

with Diagram("Graph1", show=True, outformat="png"):

    with Cluster("Public"):
        with Cluster("Public"):
            user = User("")
            device = Client("")

    with Cluster("AWS Cloud"):
        with Cluster("Web App"):
            cloudFrontD = CloudFront("CloudFront Distribution")
            lambda1 = Lambda("Lambda Function")
            s3 = S3("S3 Bucket")

        with Cluster("Processing API"):
            api = APIGateway("API Gateway")
            lambda2 = Lambda("Lambda Function")
    
    #format within Public section
    user - Edge(color="transparent") - device
    #connect within Web App section
    cloudFrontD >> Edge(style="dashed", label= "To handle large data sets a lambda \n function inspects user traffic to \n determine if a compressed version of \n the content is available to return") >> lambda1
    cloudFrontD >> Edge(style="dashed", label= "Based on the results from the lambda \n function the appropriate content is \n retrieved from the s3 bucket") >> s3
    #connect within Processing API section
    api >> Edge(style="dashed") >> lambda2

    #connect Public with AWE Cloud
    device >> Edge(color="#4472C4", label= "Users Browse the Climatch Site") >> cloudFrontD
    device >> Edge(color="#4472C4", label= "When required the site \n makes calls to a processing API ") >> api