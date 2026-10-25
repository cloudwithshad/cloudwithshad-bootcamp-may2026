# ☁️ Microsoft Azure Track | cloudwithshad Bootcamp

> **Complete, production-tested Microsoft Azure curriculum spanning Foundations, Networking, Serverless Compute, Elastic Scaling, DevOps Automation, and Applied AI.**
>
> **Curriculum Architect:** David Kumi ([@dkumi12](https://github.com/dkumi12))  
> **Course:** cloudwithshad Bootcamp · May 2026

---

## 🎯 Overview & Philosophy

The **Azure Track** provides a 1-to-1 architectural counterpart to the AWS curriculum. Every lab has been empirically verified on live Microsoft Azure infrastructure with strict adherence to **Cost Governance**, **Free-Tier Limits**, and **Production Best Practices**.

All labs use **West US 2 (`westus2`)** as the primary deployment region for guaranteed resource availability, low latency, and full support for low-cost burstable SKUs (`Standard_B1s`, `Standard_B2s`).

---

## 🗺️ AWS to Azure Curriculum Matrix

| Lab # | AWS Component (cloudwithshad) | Microsoft Azure Architecture | Lab Folder |
| :---: | :--- | :--- | :--- |
| **Lab 01** | S3 Portfolio Website | Azure Blob Storage Static Website (`$web` container) | [`lab-01-blob-portfolio/`](./lab-01-blob-portfolio/) |
| **Lab 02** | EC2 Linux Web Server | Azure Virtual Machines (Ubuntu 24.04 LTS + SSH + Nginx) | [`lab-02-vm-linux/`](./lab-02-vm-linux/) |
| **Lab 03** | VPC + RDS Two-Tier App | Azure VNet + Subnets + MySQL Flexible Server | [`lab-03-vnet-mysql/`](./lab-03-vnet-mysql/) |
| **Lab 04** | Lambda Image Resizer | Serverless Python Functions (V2 Model) + Pillow | [`lab-04-serverless-resizer/`](./lab-04-serverless-resizer/) |
| **Lab 05** | Auto-Scaling + ALB | VM Scale Set (VMSS) + Standard Load Balancer + `stress-ng` | [`lab-05-autoscaling-alb/`](./lab-05-autoscaling-alb/) |
| **Lab 06** | CI/CD Pipeline (GitHub → S3) | GitHub Actions CI/CD → Azure Blob + Front Door CDN | [`lab-06-cicd-pipeline/`](./lab-06-cicd-pipeline/) |
| **Lab 07** | Smart Document Analyzer | Document Intelligence F0 + AI Language + Cosmos DB | [`lab-07-smart-doc-analyzer/`](./lab-07-smart-doc-analyzer/) |
| **Lab 08** | AI Capstone (MarketPulse) | AI Customer Feedback Hub (HTTP API + Cosmos DB) | [`lab-08-ai-capstone/`](./lab-08-ai-capstone/) |

---

## 🔑 Key Azure Governance & Safe Operating Rules

1. **Default Region:** Always deploy resources in **`westus2`** to ensure full availability of B-series VMs and AI service endpoints.
2. **Availability Zones:** Set **Availability Zone = `None`** (*No infrastructure redundancy required*) during learning labs to avoid regional SKU restriction locks (`SKUNotAvailable`).
3. **AI Free Tiers:** Always select **Pricing Tier = `F0 (Free)`** for Document Intelligence and Language Service.
4. **Cosmos DB Free Tier:** On the Cosmos DB account creation blade, explicitly select the **"Apply"** radio button under *Apply Free Tier Discount* to receive 1000 RU/s + 25 GB free forever.
5. **Clean Up:** After completing each lab and capturing evidence screenshots, delete the Resource Group to prevent accidental charges:
   ```bash
   az group delete --name <resource-group-name> --yes --no-wait
   ```

---

*Authored with precision for the cloudwithshad engineering cohort.*
