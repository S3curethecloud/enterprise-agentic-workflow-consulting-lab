# Azure OpenAI and Microsoft Foundry Platform Mapping

## Purpose

This document maps the local lab architecture to an Azure OpenAI and Microsoft Foundry enterprise AI platform.

## Local-to-Azure Mapping

| Local Component | Azure Mapping |
|---|---|
| AI Gateway | Azure API Management, Azure AI Gateway pattern |
| Agent Orchestrator | Azure Container Apps, AKS, Durable Functions |
| RAG Service | Azure AI Search, Microsoft Fabric, Cosmos DB vector search |
| MCP Server | Azure Functions, Logic Apps, internal APIs |
| Policy Engine | Azure Policy, custom policy API, OPA on AKS |
| Evidence Store | Azure Blob Storage, Cosmos DB, Log Analytics |
| Agent Registry | Cosmos DB, Azure SQL, internal service catalog |
| Approval Service | Logic Apps, Power Automate, ServiceNow, Teams approvals |
| Observability | Azure Monitor, Application Insights, OpenTelemetry |
| Responsible AI | Azure AI Content Safety, Foundry evaluations |

## Production Architecture

```text
Enterprise App
   |
   v
Azure API Management
   |
   v
Agent Runtime on Azure Container Apps / AKS / Durable Functions
   |
   +--> Azure OpenAI / Foundry model deployment
   +--> Azure AI Search
   +--> Azure Functions tools
   +--> Policy API
   +--> Agent Registry
   +--> Approval Workflow
   +--> Evidence Store
   |
   v
Azure Monitor / App Insights / SIEM
Interview Explanation

On Azure, I would map the AI gateway to Azure API Management, the agent runtime to Container Apps or AKS, RAG to Azure AI Search, and model access to Azure OpenAI or Microsoft Foundry. Responsible AI controls can map to Azure AI Content Safety and Foundry evaluations, while approvals can be implemented through Logic Apps, Power Automate, Teams, or ServiceNow.
