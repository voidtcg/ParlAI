from aws_cdk import core
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_logs as logs
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
import os


class WebsiteStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Read environment variables for bucket name and website domain
        bucket_name = os.environ.get('BUCKET_NAME', 'my-static-website-bucket')
        website_domain = os.environ.get('WEBSITE_DOMAIN', 'example.com')
        # Assuming something.ai domain
        website_endpoint = website_domain.removesuffix('.ai')

        # Define an S3 bucket for hosting the static website
        website_bucket = s3.Bucket(self, "WebsiteBucket",
                                   bucket_name=bucket_name,
                                   website_index_document="index.html",
                                   public_read_access=True
                                   )

        # Define an origin access identity for CloudFront
        oai = cloudfront.OriginAccessIdentity(self, "WebsiteOAI")

        # Grant read permissions to the CloudFront origin access identity
        website_bucket.grant_read(oai)

        # Define a CloudFront distribution
        distribution = cloudfront.CloudFrontWebDistribution(self, "WebsiteDistribution",
                                                            origin_configs=[
                                                                cloudfront.SourceConfiguration(
                                                                    s3_origin_source=cloudfront.S3OriginConfig(
                                                                        s3_bucket_source=website_bucket,
                                                                        origin_access_identity=oai
                                                                    ),
                                                                    behaviors=[cloudfront.Behavior(is_default_behavior=True)]
                                                                )
                                                            ],
                                                            # Define the website domain as the CloudFront domain name
                                                            domain_names=[website_domain]
                                                            )

        # Create a CloudWatch Log Group for CloudFront access logs
        log_group = logs.LogGroup(self, "WebsiteLogGroup",
                                  log_group_name=f"/aws/cloudfront/{website_endpoint}WebsiteAccessLogs"
                                  )

        # Enable logging for the CloudFront distribution
        distribution.enable_logging(log_group)

        # Create a Route 53 hosted zone for the website domain
        hosted_zone = route53.HostedZone(self, "WebsiteHostedZone",
                                         zone_name=website_domain
                                         )
                
        # Create a Route 53 alias record to map the website domain to the CloudFront distribution
        route53.ARecord(self, "WebsiteAliasRecord",
                        target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
                        zone=hosted_zone,
                        record_name=website_domain
                        )

app = core.App()
WebsiteStack(app, "WebsiteStack")
app.synth()