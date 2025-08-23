#!/usr/bin/env python3
"""
Notification system for kitty - like iTerm2's notification triggers
Monitors command completion and sends macOS notifications
"""

import subprocess
import sys
import time
import os
from datetime import datetime
from typing import Optional

class KittyNotifier:
    def __init__(self):
        self.long_running_threshold = 30  # seconds
        self.error_patterns = [
            "error", "ERROR", "Error", 
            "failed", "FAILED", "Failed",
            "fatal", "FATAL", "Fatal"
        ]
    
    def send_notification(self, title: str, message: str, sound: bool = True):
        """Send macOS notification"""
        try:
            cmd = ["osascript", "-e", f'''
                display notification "{message}" with title "{title}"
            ''']
            
            if sound:
                # Add system sound
                subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"], 
                             check=False)
            
            subprocess.run(cmd, check=True)
            
        except Exception as e:
            print(f"❌ Error sending notification: {e}")
    
    def monitor_command(self, command: list, notify_on_completion: bool = True):
        """Monitor a command and send notifications based on results"""
        start_time = time.time()
        command_str = " ".join(command)
        
        try:
            # Run the command
            result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Check if command was long-running
            is_long_running = duration > self.long_running_threshold
            
            # Check for errors in output
            has_errors = any(
                pattern in result.stdout + result.stderr 
                for pattern in self.error_patterns
            )
            
            # Send notification if appropriate
            if notify_on_completion and (is_long_running or has_errors or result.returncode != 0):
                if result.returncode == 0 and not has_errors:
                    self.send_notification(
                        "✅ Command Completed",
                        f"'{command_str}' finished in {duration:.1f}s"
                    )
                else:
                    self.send_notification(
                        "❌ Command Failed", 
                        f"'{command_str}' failed (exit code: {result.returncode})",
                        sound=True
                    )
            
            # Output the results
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)
            
            return result.returncode
            
        except KeyboardInterrupt:
            self.send_notification(
                "⏹️ Command Interrupted",
                f"'{command_str}' was interrupted"
            )
            return 130
            
        except Exception as e:
            self.send_notification(
                "💥 Command Error",
                f"Error running '{command_str}': {e}"
            )
            return 1
    
    def wrap_shell_command(self, shell_command: str):
        """Wrap a shell command with monitoring"""
        return self.monitor_command(["sh", "-c", shell_command])
    
    def notify_on_background_job_completion(self):
        """Check for completed background jobs and notify"""
        try:
            # Get list of jobs
            result = subprocess.run(
                ["jobs"], 
                shell=True,
                capture_output=True, 
                text=True
            )
            
            if result.stdout.strip():
                # Parse job output and check status
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if "Done" in line or "Exit" in line:
                        self.send_notification(
                            "🎯 Background Job Complete",
                            f"Job finished: {line}"
                        )
                        
        except Exception as e:
            print(f"Error checking background jobs: {e}")

def main():
    notifier = KittyNotifier()
    
    if len(sys.argv) < 2:
        print("Usage: notify <command> [args...]")
        print("       notify --jobs  # Check background jobs")
        print("       notify --test  # Send test notification")
        sys.exit(1)
    
    if sys.argv[1] == "--jobs":
        notifier.notify_on_background_job_completion()
    
    elif sys.argv[1] == "--test":
        notifier.send_notification(
            "🧪 Test Notification", 
            "Kitty notification system is working!"
        )
    
    else:
        # Monitor the provided command
        command = sys.argv[1:]
        exit_code = notifier.monitor_command(command)
        sys.exit(exit_code)

if __name__ == "__main__":
    main()