"""
AI Integration for Email Parser using Ollama
Provides AI-powered analysis using local Phi3 model
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass

try:
    import ollama
    import requests
except ImportError:
    print("Warning: AI dependencies not installed. Install with: uv pip install \".[ai]\"")
    ollama = None
    requests = None

from .parser import EmailContent

logger = logging.getLogger(__name__)

@dataclass
class AIAnalysisResult:
    """Result from AI analysis"""
    summary: str
    categories: List[str]
    sentiment: str
    priority_score: float
    key_insights: List[str]
    action_items: List[str]
    confidence: float
    model_used: str

class OllamaEmailAnalyzer:
    """AI-powered email analyzer using Ollama Phi3"""
    
    def __init__(self, model_name: str = "phi3", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Ollama client and check model availability"""
        if ollama is None or requests is None:
            logger.error("AI dependencies not available. Install with: uv pip install \".[ai]\"")
            return False
        
        try:
            # Test connection to Ollama
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code != 200:
                logger.error(f"Cannot connect to Ollama at {self.host}")
                return False
            
            # Check if model is available
            models = response.json()
            available_models = [model['name'] for model in models.get('models', [])]
            
            if not any(self.model_name in model for model in available_models):
                logger.warning(f"Model {self.model_name} not found. Available models: {available_models}")
                logger.info(f"To install Phi3, run: ollama pull {self.model_name}")
                return False
            
            self.client = ollama.Client(host=self.host)
            logger.info(f"Successfully connected to Ollama with model {self.model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Ollama client: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if AI analysis is available"""
        return self.client is not None
    
    def analyze_email(self, email_content: EmailContent) -> Optional[AIAnalysisResult]:
        """Perform comprehensive AI analysis of email content"""
        if not self.is_available():
            logger.error("AI analysis not available")
            return None
        
        try:
            # Prepare email content for analysis
            content_text = self._prepare_email_text(email_content)
            
            # Run analysis
            summary = self._generate_summary(content_text)
            categories = self._classify_categories(content_text)
            sentiment = self._analyze_sentiment(content_text)
            priority_score = self._calculate_priority(content_text)
            key_insights = self._extract_insights(content_text)
            action_items = self._extract_action_items(content_text)
            
            return AIAnalysisResult(
                summary=summary,
                categories=categories,
                sentiment=sentiment,
                priority_score=priority_score,
                key_insights=key_insights,
                action_items=action_items,
                confidence=0.85,  # Default confidence
                model_used=self.model_name
            )
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return None
    
    def _prepare_email_text(self, email_content: EmailContent) -> str:
        """Prepare email content for AI analysis"""
        parts = []
        
        if email_content.subject:
            parts.append(f"Subject: {email_content.subject}")
        
        if email_content.sender:
            parts.append(f"From: {email_content.sender}")
        
        if email_content.recipients:
            parts.append(f"To: {', '.join(email_content.recipients[:3])}")
        
        if email_content.body_text:
            # Limit body text to reasonable size for analysis
            body = email_content.body_text[:2000]
            if len(email_content.body_text) > 2000:
                body += "... [truncated]"
            parts.append(f"Content: {body}")
        
        if email_content.attachments:
            att_names = [att.get('filename', 'unnamed') for att in email_content.attachments[:5]]
            parts.append(f"Attachments: {', '.join(att_names)}")
        
        return "\n\n".join(parts)
    
    def _generate_summary(self, content: str) -> str:
        """Generate AI-powered email summary"""
        prompt = f"""
Analyze this email and provide a concise 2-3 sentence summary focusing on the main purpose and key information:

{content}

Summary:"""

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "max_tokens": 200
                }
            )
            
            summary = response['response'].strip()
            return summary if summary else "Unable to generate summary"
            
        except Exception as e:
            logger.error(f"Summary generation failed: {e}")
            return "AI summary unavailable"
    
    def _classify_categories(self, content: str) -> List[str]:
        """AI-powered email categorization"""
        prompt = f"""
Classify this email into relevant categories. Choose from these options:
- meeting: Meeting requests, scheduling, calendar invites
- urgent: Time-sensitive, high priority communications
- invoice: Billing, payments, financial transactions
- report: Status updates, analytics, summaries
- support: Help requests, troubleshooting, customer service
- contract: Legal documents, agreements, terms
- follow_up: Reminders, check-ins, status requests
- notification: System alerts, automated messages
- marketing: Promotional content, newsletters, announcements
- personal: Non-business, casual communication

Email content:
{content}

Return only the category names that apply, separated by commas:"""

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.2,
                    "max_tokens": 100
                }
            )
            
            categories_text = response['response'].strip()
            # Parse categories from response
            categories = [cat.strip().lower() for cat in categories_text.split(',') if cat.strip()]
            
            # Validate categories
            valid_categories = {
                'meeting', 'urgent', 'invoice', 'report', 'support', 
                'contract', 'follow_up', 'notification', 'marketing', 'personal'
            }
            
            return [cat for cat in categories if cat in valid_categories] or ['general']
            
        except Exception as e:
            logger.error(f"Category classification failed: {e}")
            return ['general']
    
    def _analyze_sentiment(self, content: str) -> str:
        """Analyze email sentiment"""
        prompt = f"""
Analyze the sentiment/tone of this email. Respond with one word only:
- positive: Friendly, enthusiastic, appreciative
- negative: Angry, frustrated, complaining
- neutral: Professional, factual, informative
- concerned: Worried, cautious, seeking clarification

Email content:
{content}

Sentiment:"""

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.1,
                    "max_tokens": 20
                }
            )
            
            sentiment = response['response'].strip().lower()
            valid_sentiments = {'positive', 'negative', 'neutral', 'concerned'}
            
            return sentiment if sentiment in valid_sentiments else 'neutral'
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return 'neutral'
    
    def _calculate_priority(self, content: str) -> float:
        """Calculate email priority score using AI"""
        prompt = f"""
Rate the priority/urgency of this email on a scale from 0.0 to 1.0:
- 0.0-0.3: Low priority (FYI, newsletters, routine updates)
- 0.4-0.6: Medium priority (regular business, non-urgent requests)
- 0.7-0.9: High priority (time-sensitive, important decisions)
- 0.9-1.0: Critical priority (emergencies, immediate action required)

Consider factors like:
- Urgency keywords (urgent, ASAP, immediate, critical)
- Deadlines and time constraints
- Business impact and importance
- Sender authority and context

Email content:
{content}

Priority score (just the number):"""

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.2,
                    "max_tokens": 20
                }
            )
            
            score_text = response['response'].strip()
            
            # Extract number from response
            import re
            numbers = re.findall(r'\d*\.?\d+', score_text)
            if numbers:
                score = float(numbers[0])
                return max(0.0, min(1.0, score))  # Clamp between 0 and 1
            
            return 0.5  # Default medium priority
            
        except Exception as e:
            logger.error(f"Priority calculation failed: {e}")
            return 0.5
    
    def _extract_insights(self, content: str) -> List[str]:
        """Extract key insights from email"""
        prompt = f"""
Extract 2-4 key insights or important points from this email. Focus on:
- Main topics or themes
- Important information or data points
- Notable requests or requirements
- Significant context or background

Email content:
{content}

Key insights (one per line, starting with "-"):"""

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.4,
                    "max_tokens": 300
                }
            )
            
            insights_text = response['response'].strip()
            
            # Parse insights from response
            insights = []
            for line in insights_text.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    insight = line[1:].strip()
                    if insight:
                        insights.append(insight)
            
            return insights[:4]  # Limit to 4 insights
            
        except Exception as e:
            logger.error(f"Insight extraction failed: {e}")
            return []
    
    def _extract_action_items(self, content: str) -> List[str]:
        """Extract action items from email"""
        prompt = f"""
Identify specific action items or tasks mentioned in this email. Look for:
- Explicit requests ("please do", "need you to", "can you")
- Deadlines and deliverables
- Follow-up requirements
- Tasks that need completion

Email content:
{content}

Action items (one per line, starting with "-", max 5):"""

        try:
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.3,
                    "max_tokens": 300
                }
            )
            
            actions_text = response['response'].strip()
            
            # Parse action items from response
            actions = []
            for line in actions_text.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    action = line[1:].strip()
                    if action:
                        actions.append(action)
            
            return actions[:5]  # Limit to 5 action items
            
        except Exception as e:
            logger.error(f"Action item extraction failed: {e}")
            return []
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze arbitrary text (for CLI/API use)"""
        if not self.is_available():
            return {"error": "AI analysis not available"}
        
        try:
            # Create a minimal email content object
            from dataclasses import dataclass
            from datetime import datetime
            
            @dataclass
            class TextContent:
                subject: str = ""
                sender: str = ""
                recipients: List[str] = None
                body_text: str = ""
                attachments: List[Dict] = None
                
                def __post_init__(self):
                    if self.recipients is None:
                        self.recipients = []
                    if self.attachments is None:
                        self.attachments = []
            
            # Treat text as email body
            text_content = TextContent(body_text=text)
            
            summary = self._generate_summary(text)
            categories = self._classify_categories(text)
            sentiment = self._analyze_sentiment(text)
            priority_score = self._calculate_priority(text)
            key_insights = self._extract_insights(text)
            action_items = self._extract_action_items(text)
            
            return {
                "summary": summary,
                "categories": categories,
                "sentiment": sentiment,
                "priority_score": priority_score,
                "key_insights": key_insights,
                "action_items": action_items,
                "confidence": 0.85,
                "model_used": self.model_name
            }
            
        except Exception as e:
            logger.error(f"Text analysis failed: {e}")
            return {"error": str(e)}

# Convenience function
def create_ai_analyzer(model_name: str = "phi3") -> Optional[OllamaEmailAnalyzer]:
    """Create and initialize AI analyzer"""
    analyzer = OllamaEmailAnalyzer(model_name)
    if analyzer.is_available():
        return analyzer
    return None