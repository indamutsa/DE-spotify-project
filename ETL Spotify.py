import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Artists
Artists_node1708875923521 = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": ["s3://project-spotify-madrid/staging/artists.csv"],
        "recurse": True,
    },
    transformation_ctx="Artists_node1708875923521",
)

# Script generated for node Albums
Albums_node1708875924141 = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": ["s3://project-spotify-madrid/staging/albums.csv"],
        "recurse": True,
    },
    transformation_ctx="Albums_node1708875924141",
)

# Script generated for node tracks
tracks_node1708875924676 = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": ["s3://project-spotify-madrid/staging/track.csv"],
        "recurse": True,
    },
    transformation_ctx="tracks_node1708875924676",
)

# Script generated for node Join Artists & Albums
JoinArtistsAlbums_node1708875989145 = Join.apply(
    frame1=Artists_node1708875923521,
    frame2=Albums_node1708875924141,
    keys1=["id"],
    keys2=["artist_id"],
    transformation_ctx="JoinArtistsAlbums_node1708875989145",
)

# Script generated for node Join Album& Artists -- Tracks
JoinAlbumArtistsTracks_node1708876171118 = Join.apply(
    frame1=tracks_node1708875924676,
    frame2=JoinArtistsAlbums_node1708875989145,
    keys1=["track_id"],
    keys2=["track_id"],
    transformation_ctx="JoinAlbumArtistsTracks_node1708876171118",
)

# Script generated for node Drop Fields
DropFields_node1708876296701 = DropFields.apply(
    frame=JoinAlbumArtistsTracks_node1708876171118,
    paths=["`.track_id`", "id"],
    transformation_ctx="DropFields_node1708876296701",
)

# Script generated for node Destination
Destination_node1708876407455 = glueContext.write_dynamic_frame.from_options(
    frame=DropFields_node1708876296701,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://project-spotify-madrid/data-warehouse/",
        "partitionKeys": [],
    },
    format_options={"compression": "snappy"},
    transformation_ctx="Destination_node1708876407455",
)

job.commit()