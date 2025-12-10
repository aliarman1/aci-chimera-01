"""
Rate limiter to prevent exceeding Gemini API quotas
"""
import time
from collections import deque
from typing import Optional

class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_requests_per_minute: int = 15):
        """
        Initialize rate limiter
        
        Args:
            max_requests_per_minute: Maximum requests allowed per minute (default: 15 for free tier)
        """
        self.max_requests = max_requests_per_minute
        self.requests = deque()
        
    def wait_if_needed(self) -> Optional[float]:
        """
        Check if we need to wait before making another request.
        Returns the number of seconds waited, or None if no wait was needed.
        """
        current_time = time.time()
        
        # Remove requests older than 60 seconds
        while self.requests and current_time - self.requests[0] > 60:
            self.requests.popleft()
        
        # Check if we've hit the limit
        if len(self.requests) >= self.max_requests:
            # Calculate how long to wait
            oldest_request = self.requests[0]
            wait_time = 60 - (current_time - oldest_request)
            
            if wait_time > 0:
                print(f"⏳ Rate limit reached. Waiting {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                return wait_time
        
        # Record this request
        self.requests.append(current_time)
        return None
    
    def get_remaining_requests(self) -> int:
        """Get number of remaining requests in current window"""
        current_time = time.time()
        
        # Remove old requests
        while self.requests and current_time - self.requests[0] > 60:
            self.requests.popleft()
        
        return max(0, self.max_requests - len(self.requests))

# Global rate limiter instance
# Free tier: 15 RPM, Paid tier: 1000 RPM
rate_limiter = RateLimiter(max_requests_per_minute=15)
