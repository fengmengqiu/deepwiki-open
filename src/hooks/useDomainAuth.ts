import { useState, useEffect } from 'react';

interface DomainAuthResponse {
  has_domain_auth: boolean;
  domain: string | null;
  message: string;
}

/**
 * Check if repository URL has configured domain authentication
 *
 * @param repoUrl Repository URL
 * @returns Domain authentication status and loading state
 */
export function useDomainAuth(repoUrl: string) {
  const [domainAuth, setDomainAuth] = useState<DomainAuthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Reset state for invalid or empty URLs
    if (!repoUrl || !repoUrl.includes('://')) {
      setDomainAuth(null);
      return;
    }

    const checkDomain = async () => {
      setIsLoading(true);

      try {
        const response = await fetch('/api/git/check-domain', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ repo_url: repoUrl }),
        });

        if (response.ok) {
          const data = await response.json();
          setDomainAuth(data);
        } else {
          // Assume no domain auth on API error
          setDomainAuth({
            has_domain_auth: false,
            domain: null,
            message: ''
          });
        }
      } catch (err) {
        console.error('Error checking domain authentication:', err);
        setDomainAuth({
          has_domain_auth: false,
          domain: null,
          message: ''
        });
      } finally {
        setIsLoading(false);
      }
    };

    // Debounce: avoid triggering request on every keystroke
    const timeoutId = setTimeout(checkDomain, 500);

    return () => clearTimeout(timeoutId);
  }, [repoUrl]);

  return { domainAuth, isLoading };
}
