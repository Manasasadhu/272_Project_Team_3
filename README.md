## Manasa's Project Proposal 

⸻

📄 Project Proposal: **AI Mental Health & Burnout Management Platform**

1. Problem Statement

In the United States, workplace stress and burnout are major daily issues. According to the American Psychological Association, over 75% of employees report stress negatively impacting their mental health, yet access to support remains limited due to stigma, cost, or lack of resources.

For enterprises, unmanaged burnout leads to lower productivity, absenteeism, and high employee turnover, costing billions annually.
Current wellness solutions are fragmented, generic, and fail to integrate seamlessly into daily workplace tools.

⸻

2. Proposed Solution

I propose an **AI-powered mental health and burnout management platform** designed for enterprises. The platform combines personalized employee support with enterprise analytics, ensuring both individual well-being and organizational insight.

Key Features
	•	AI Wellness Agent
	•	Daily mood check-ins via chat.
	•	Personalized coping strategies (meditation, focus exercises, break scheduling).
	•	Journaling with AI summaries for self-reflection.
	•	Therapist Connection (Optional)
	•	Secure channel for licensed professional sessions when needed.
	•	Burnout Risk Detection
	•	Sentiment analysis of interactions.
	•	AI predicts burnout trends based on mood and activity patterns.
	•	Enterprise Dashboard
	•	HR/management view (anonymized): workforce engagement, stress levels, burnout risk.
	•	Helps companies take preventive action (wellness programs, workload adjustments).

⸻

3. Enterprise Impact
	•	Employees: Accessible, stigma-free mental health support available anytime.
	•	Employers: Lower turnover, higher productivity, and stronger employee engagement.
	•	Compliance: Can support HIPAA standards for secure data handling.

⸻

4. Technology Stack (Prototype)
	•	Frontend: React (Web), Flutter (Mobile)
	•	Backend: Node.js / Flask
	•	Database: MongoDB (journaling, mood logs), PostgreSQL (enterprise analytics)
	•	AI Layer:
	•	GPT-based conversational AI for chat support
	•	Hugging Face models for sentiment/mood analysis
	•	Integrations: Slack, Microsoft Teams, Google Workspace
	•	Deployment: Cloud-based SaaS (AWS/GCP)

⸻

5. Scope for Expansion
	•	Personalized wellness roadmaps for employees.
	•	Integration with wearable devices (Fitbit, Apple Watch) for real-time stress tracking.
	•	Enterprise benchmarking of wellness KPIs across industries.

⸻


## Samved's project proposal

Project Proposal: Academic Literature Review Agent
Course: Enterprise Software Platform (MSSE CMPE 272a0


1. Abstract and Problem Statement

   A. The Problem Graduate students and researchers face a significant bottleneck in the research process: the manual, time-intensive labor of searching, filtering, and synthesizing academic literature. This process often involves juggling multiple sources, applying inconsistent filtering criteria, and is prone to human oversight, preventing researchers from keeping pace with the rapid growth of published material. This is a reactive workflow.


     B. The Agentic Solution
We propose the Academic Literature Review Agent, an autonomous, decision-making ecosystem  designed to transform this manual workflow into a proactive, scalable platform. The agent's core function is to perceive a high-level research topic, employ goal-oriented reasoning  to identify authoritative sources, and autonomously synthesize the findings into a cohesive, structured report. The system shifts software from merely responding to user input to actively initiating and executing complex tasks.


    C. Expected Impact
The project will serve as a definitive proof-of-concept for autonomous enterprise capabilities, significantly reducing the time required for a literature review while simultaneously ensuring auditability and rigor through controlled, governed decision-making.



2. Agent Workflow and Autonomous Execution
The agent operates on the principle of the ReAct (Reasoning and Acting) loop, enabling it to make decisions and initiate actions without explicit human commands.

A. The Four-Step Autonomous Pipeline
1. Search & Refinement (Perceiving Context): The agent first uses Tool 1 (Search API) to gather relevant sources. It then uses its LLM core to reason about the quality and relevance of the initial search results, dynamically modifying the search query if the initial results fail to meet academic standards.

2. Filter & Rank (Making Decisions): Based on the Master System Prompt (our set of business rules), the agent filters out low-authority sources (e.g., non-peer-reviewed blogs) and ranks the remaining papers. This dynamic filtering prevents waste of computational resources and ensures output reliability.

3. Process & Structure (Autonomous Execution): The agent iteratively calls Tool 2 (Summarization Service) on each highly ranked source. This tool fetches and cleans the article text, then uses the LLM to generate a structured output focusing exclusively on academic details (Methodology, Key Findings).

4. Synthesize & Deliver (Adaptation): After gathering all structured data, the agent performs a final synthesis, creating a cohesive, structured report that highlights common themes, conflicts, and research gaps, thus fulfilling the user's high-level research goal. If any step fails (e.g., a paywall is encountered), the agent reasons about the failure and attempts to replans its search, demonstrating continuous learning and adaptation.

B. Novelty and Defense Against Market Solutions
While market tools exist, they operate as Fixed Chains (reactive execution of a set script). This agent is proactive  and necessary because: It demonstrates tool orchestration by chaining non-LLM services (Search API) with LLM-assisted services (Structured Summarization). It enforces custom governance rules (source reliability, specific synthesis structure) that are not available in off-the-shelf tools. It exposes the audit trail (the LLM's Thought process) for every autonomous decision, a necessity for enterprise-grade compliance.



<img width="724" height="141" alt="image" src="https://github.com/user-attachments/assets/6ffceffe-d554-4921-9ec6-be0cf8f722a7" />





## Personalized Health Dashboard - Tin's Project proposal 

People generate massive amounts of health data from wearables, smartphones, and connected devices, but most apps only display raw numbers (steps, calories, heart rate) without meaningful context. Users often struggle to understand what these numbers mean for their long-term health, and physicians rarely have the time or tools to translate fragmented lifestyle data into preventive care insights. 

The objective of this project is to build a Personalized Health Dashboard that converts wearable and phone-synced data into predictive insights and actionable guidance. By leveraging machine learning, the system will identify early health risks, explain the contributing factors in clear language, and provide personalized recommendations to keep users on track with their fitness and wellness goals.

<img width="921" height="424" alt="Screenshot 2025-10-01 at 12 12 48 AM" src="https://github.com/user-attachments/assets/ba7f85fb-5b50-48f7-85cf-1a43f124a481" />


