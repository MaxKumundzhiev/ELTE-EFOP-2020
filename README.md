# [WIP] ELTE-EFOP-2020
## :rotating_light: Under development
Developing Approaches for Estimating Models Based on Hyper Graphs within Dynamic Business Processes.

# AWS Tools Usage
1. AWS S3
2. AWS Lambda
3. AWS DynamoDB
4. AWS Gateway API 

# Scheme
![Wavelength image 1a](https://user-images.githubusercontent.com/37558223/78239597-2fb25700-74de-11ea-91fe-aaff905759b2.png)


# Tools
<ul>
<h2>S3 Data Uploader</h2>
The tool assumed to download data from TFL and upload to the dedicated S3 Bucket

#### Get help: 
````bash
cd s3_upload && python handler.py -h   
````
#### Run the Script: 
````bash
cd s3_upload && python handler.py --id --key --year  
````
#### Example: 
````bash
cd s_upload && python handler.py --id tfl_id --key tfl_key --year 2020  
````
</ul>

# Docker deployment
### Download Docker Image from DockerHub

### Build Docker Image
```bash
docker build -t hypergraph .
```
where <t> - name of Docker Image,  <.> path to entrypoint

### Run Docker Image <Container>
```bash
docker run --rm --name efop -d  hypergraph
```
where : 
<name>  -  name of Docker Container,
<hypergraph> - name of Docker Image;
<-d> - run in background mode;
<--rm> - remove Docker Container after execution;





<b>References:</b><br>
<ul>
<li><a href="https://machinelearningmastery.com/estimate-performance-machine-learning-algorithms-weka/">WEKA</a></li>
  <li><a href="https://drive.google.com/file/d/1Bo1c6BJNfdim81CWp7VbqLNkP3RAawGk/view?ts=5e55708d">Data Scheme</a></li>
  <li><a href="https://www.researchgate.net/publication/273462758_Hadoop_Performance_Modeling_for_Job_Estimation_and_Resource_Provisioning">Hadoop Performance Paper</a></li>
</ul>


<b>Supervised by : Balint Molnar</b><br>
<b>Participantes : Khawla Bouafia, Maksim Kumundzhiev</b>


## Topics
|Paper|Code|Tutorial|Any Other links|
|-----|----|--------|---------------|


## IAM

**[Malsim Kumundzhiev](https://github.com/KumundzhievMaxim)**

[<img src="http://i.imgur.com/0o48UoR.png" width="35">](https://github.com/KumundzhievMaxim)             [<img src="https://i.imgur.com/0IdggSZ.png" width="35">](https://www.linkedin.com/in/maksim-kumundzhiev/)             [<img src="https://loading.io/s/icon/vzeour.svg" width="35">](https://www.kaggle.com/maximkumundzhiev)               
