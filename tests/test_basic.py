#!/usr/bin/env python3
"""
Debug tests for email parser with detailed output
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def test_import():
    """Test that we can import the parser"""
    try:
        from email_parser.parser import EmailParser
        parser = EmailParser()
        assert parser is not None
        assert parser.supported_extensions == ['.msg']
        print("✅ Basic import test passed")
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        print("Current Python path:")
        for p in sys.path:
            print(f"  {p}")
        return False

def test_entity_patterns_debug():
    """Test entity pattern extraction with debug output"""
    try:
        from email_parser.parser import EmailParser
        
        parser = EmailParser()
        text = "Contact john@example.com or call 555-123-4567. Budget is $10,000."
        
        print(f"📝 Test text: {text}")
        print(f"🔍 Entity patterns: {list(parser.entity_patterns.keys())}")
        
        entities = parser._extract_entities(text)
        
        print(f"📊 Extracted entities:")
        for entity_type, items in entities.items():
            print(f"  {entity_type}: {items}")
        
        # Check each entity type
        email_found = 'john@example.com' in entities.get('emails', [])
        phone_found = any('555' in str(p) for p in entities.get('phones', []))
        money_found = any('10,000' in str(m) for m in entities.get('money', []))
        
        print(f"🔍 Checks:")
        print(f"  Email found: {email_found}")
        print(f"  Phone found: {phone_found}")
        print(f"  Money found: {money_found}")
        
        if email_found and phone_found and money_found:
            print("✅ Entity extraction test passed")
            return True
        else:
            print("❌ Entity extraction test failed - some entities not found")
            return False
            
    except Exception as e:
        print(f"❌ Entity extraction test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_patterns():
    """Test each pattern individually"""
    try:
        from email_parser.parser import EmailParser
        import re
        
        parser = EmailParser()
        
        test_cases = {
            'emails': ('john@example.com', 'Contact john@example.com today'),
            'phones': ('555-123-4567', 'Call 555-123-4567 for support'),
            'money': ('$10,000', 'Budget is $10,000 for this project'),
            'urls': ('https://example.com', 'Visit https://example.com for info'),
            'dates': ('12/31/2024', 'Deadline is 12/31/2024')
        }
        
        print("🧪 Testing individual patterns:")
        
        all_passed = True
        for pattern_name, (expected, test_text) in test_cases.items():
            pattern = parser.entity_patterns[pattern_name]
            matches = re.findall(pattern, test_text, re.IGNORECASE)
            
            found = expected in matches
            print(f"  {pattern_name}: {'✅' if found else '❌'} Expected '{expected}', found {matches}")
            
            if not found:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Individual pattern test failed: {e}")
        return False

def test_correlation_calculation():
    """Test correlation calculation"""
    try:
        from email_parser.parser import EmailParser
        
        parser = EmailParser()
        
        # Test high correlation
        subject = "Meeting agenda items"
        body = "Here are the meeting agenda items for discussion"
        attachments = []
        
        score = parser._calculate_correlation(subject, body, attachments)
        assert score > 0.3, f"Expected correlation > 0.3, got {score}"
        
        print(f"✅ Correlation calculation test passed (score: {score:.3f})")
        return True
    except Exception as e:
        print(f"❌ Correlation calculation test failed: {e}")
        return False

def test_categorization():
    """Test email categorization"""
    try:
        from email_parser.parser import EmailParser
        
        parser = EmailParser()
        
        # Test meeting categorization
        subject = "Weekly team meeting"
        body = "Let's schedule our weekly meeting for Tuesday"
        attachments = []
        
        categories = parser._categorize_email(subject, body, attachments)
        assert 'meeting' in categories, f"Expected 'meeting' in categories, got {categories}"
        
        print(f"✅ Email categorization test passed (categories: {categories})")
        return True
    except Exception as e:
        print(f"❌ Email categorization test failed: {e}")
        return False

def test_full_parsing_workflow():
    """Test the complete parsing workflow without .msg file"""
    try:
        from email_parser.parser import EmailParser
        
        parser = EmailParser()
        
        # Test all the helper methods
        print("🔄 Testing full workflow components:")
        
        # Test recipient parsing
        recipients = parser._parse_recipients("john@example.com, jane@example.com; bob@test.com")
        print(f"  Recipients parsing: {recipients}")
        assert len(recipients) == 3
        
        # Test summary generation
        subject = "Important project update"
        body = "This is the first sentence of the email. Here's more content that follows."
        summary = parser._generate_summary(subject, body)
        print(f"  Summary generation: {summary}")
        
        # Test key points extraction
        body_with_bullets = """
        Here are the key points:
        • First important point
        • Second key item
        1. Numbered item one
        2. Numbered item two
        Please note this is important.
        """
        key_points = parser._extract_key_points(body_with_bullets)
        print(f"  Key points: {key_points}")
        
        # Test action items
        body_with_actions = "Please review the document by Friday. You need to call the client."
        actions = parser._extract_action_items(body_with_actions)
        print(f"  Action items: {actions}")
        
        print("✅ Full workflow test passed")
        return True
        
    except Exception as e:
        print(f"❌ Full workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔬 Email Parser Debug Tests")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_import),
        ("Individual Patterns", test_individual_patterns),
        ("Entity Extraction Debug", test_entity_patterns_debug),
        ("Correlation Calculation", test_correlation_calculation),
        ("Email Categorization", test_categorization),
        ("Full Workflow", test_full_parsing_workflow),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 30)
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                failed += 1
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"💥 {test_name} CRASHED: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Final Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The email parser is working correctly.")
        print("\n🚀 Ready to process .msg files!")
        print("Next steps:")
        print("  1. Add .msg files to examples/sample_emails/")
        print("  2. Run: python -m src.email_parser.main")
    else:
        print(f"⚠️  {failed} test(s) failed - check the output above")
    
    sys.exit(0 if failed == 0 else 1)