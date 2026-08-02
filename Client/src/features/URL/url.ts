export interface ShortenUrlRequest {
  url: string;
  expiry_days?: number;
}

export interface ShortenUrlResponse {
  short_code: string;
  short_url: string;
  original_url: string;
  created_at: string;
  expires_at?: string | null;
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function normalizeUrl(value: string) {
  const trimmedValue = value.trim();
  if (!trimmedValue) {
    return trimmedValue;
  }

  return /^https?:\/\//i.test(trimmedValue)
    ? trimmedValue
    : `https://${trimmedValue}`;
}

export async function shortenUrl(longUrl: string, expiryDays?: number) {
  const payload: ShortenUrlRequest = {
    url: normalizeUrl(longUrl),
    ...(expiryDays != null ? { expiry_days: expiryDays } : {}),
  };

  const response = await fetch(`${API_BASE_URL}/api/shorten`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(
      errorText || `Request failed with status ${response.status}`,
    );
  }

  return (await response.json()) as ShortenUrlResponse;
}
