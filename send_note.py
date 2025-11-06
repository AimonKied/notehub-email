#!/usr/bin/env python3
"""
Email Sender for Notehub Notes
Finds the newest text file in ../notehub/notes and sends it via email
"""

import os
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path


def load_env():
    """
    Load environment variables from .env file
    """
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    env_vars = {}
    
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
    
    return env_vars


def get_latest_note(notes_dir):
    """
    Find the most recent text file in the notes directory
    """
    # Search for all .txt files recursively
    txt_files = glob.glob(os.path.join(notes_dir, "**/*.txt"), recursive=True)
    
    if not txt_files:
        return None
    
    # Get the most recent file based on modification time
    latest_file = max(txt_files, key=os.path.getmtime)
    return latest_file


def read_note(file_path):
    """
    Read the content of a note file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def send_email(subject, body, from_email, to_email, password, smtp_server="smtp.gmail.com", smtp_port=587, username=None):
    """
    Send an email with the note content
    
    Args:
        subject: Email subject
        body: Email body (note content)
        from_email: Sender email address
        to_email: Recipient email address
        password: Email password or app-specific password
        smtp_server: SMTP server address (default: Gmail)
        smtp_port: SMTP port (default: 587 for TLS)
        username: Optional username for SMTP login (if different from from_email)
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Create SMTP session
        print(f"   🔌 Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.set_debuglevel(0)  # Set to 1 for verbose debugging
        
        print(f"   🔒 Starting TLS encryption...")
        server.starttls()  # Enable security
        
        # Login (use username if provided, otherwise use from_email)
        login_user = username if username else from_email
        print(f"   🔑 Logging in as: {login_user}")
        server.login(login_user, password)
        
        # Send email
        print(f"   📤 Sending email...")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print(f"✅ Email successfully sent to {to_email}")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check if your password is correct")
        print("   2. For All-Inkl: Make sure SMTP is enabled in your email settings")
        print("   3. Some providers require a username instead of email address")
        print("   4. Check if 2FA is enabled (may require app password)")
        return False
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def main():
    """
    Main function to find latest note and send it via email
    """
    # Load environment variables
    env = load_env()
    
    # Configuration
    NOTES_DIR = os.path.join(os.path.dirname(__file__), "../notehub/notes")
    NOTES_DIR = os.path.abspath(NOTES_DIR)
    
    print("📧 Notehub Email Sender")
    print("=" * 50)
    
    # Find latest note
    print(f"🔍 Searching for notes in: {NOTES_DIR}")
    latest_note = get_latest_note(NOTES_DIR)
    
    if not latest_note:
        print("❌ No notes found!")
        return
    
    # Get file info
    file_name = os.path.basename(latest_note)
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_note))
    
    print(f"\n📝 Latest note found:")
    print(f"   File: {file_name}")
    print(f"   Path: {latest_note}")
    print(f"   Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Read note content
    content = read_note(latest_note)
    if not content:
        print("❌ Could not read note content!")
        return
    
    print(f"\n📄 Note preview (first 200 chars):")
    print("-" * 50)
    print(content[:200] + ("..." if len(content) > 200 else ""))
    print("-" * 50)
    
    # Ask user if they want to send
    print("\n❓ Do you want to send this note via email?")
    response = input("   Type 'yes' or 'y' to continue: ").lower().strip()
    
    if response not in ['yes', 'y']:
        print("❌ Email sending cancelled.")
        return
    
    # Get email configuration from .env or prompt user
    print("\n📧 Email Configuration:")
    
    # Check if .env file has credentials
    if env.get('FROM_EMAIL') and env.get('TO_EMAIL') and env.get('EMAIL_PASSWORD'):
        print("   ✅ Using credentials from .env file")
        from_email = env['FROM_EMAIL']
        to_email = env['TO_EMAIL']
        password = env['EMAIL_PASSWORD']
        smtp_server = env.get('SMTP_SERVER', 'smtp.all-inkl.com')
        smtp_port = int(env.get('SMTP_PORT', '587'))
        
        print(f"   From: {from_email}")
        print(f"   To: {to_email}")
        print(f"   SMTP: {smtp_server}:{smtp_port}")
        
        # Option to override
        override = input("\n   Use different settings? (y/n, default: n): ").lower().strip()
        if override == 'y':
            from_email = input("   From email: ").strip()
            to_email = input("   To email: ").strip()
            password = input("   Email password: ").strip()
    else:
        print("   ⚠️  No .env file found or incomplete. Please enter credentials:")
        from_email = input("   From email: ").strip()
        to_email = input("   To email: ").strip()
        password = input("   Email password: ").strip()
        smtp_server = env.get('SMTP_SERVER', 'smtp.all-inkl.com')
        smtp_port = int(env.get('SMTP_PORT', '587'))
    
    # Optional: custom SMTP settings (only if not using .env defaults)
    if not (env.get('FROM_EMAIL') and env.get('TO_EMAIL') and env.get('EMAIL_PASSWORD')):
        use_custom = input("   Use custom SMTP settings? (y/n, default: n for All-Inkl): ").lower().strip()
        
        if use_custom == 'y':
            smtp_server = input(f"   SMTP server (default: {smtp_server}): ").strip() or smtp_server
            smtp_port = input(f"   SMTP port (default: {smtp_port}): ").strip() or str(smtp_port)
            smtp_port = int(smtp_port)
    
    # Get optional SMTP username (if different from email)
    smtp_username = env.get('SMTP_USERNAME')
    
    # Prepare subject
    subject = f"Notehub Note: {file_name}"
    
    # Send email
    print("\n📤 Sending email...")
    success = send_email(
        subject=subject,
        body=content,
        from_email=from_email,
        to_email=to_email,
        password=password,
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        username=smtp_username
    )
    
    if success:
        print("\n✅ Done!")
    else:
        print("\n❌ Failed to send email. Please check your credentials and settings.")


if __name__ == "__main__":
    main()
