import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

export let errorRate = new Rate("errors");

// Configuration for load testing stages
// Customize these stages based on your testing needs:
// - duration: how long each stage lasts
// - target: number of virtual users for that stage
export let options = {
  stages: [
    { duration: "15m", target: 500 }, // Stay at 500 users for 15 minutes
  ],
};

const BASE_URL = "http://py-url-shortener:8000";

export default function () {
  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  // Test POST /short-key

  let response1 = http.post(
    `${BASE_URL}/short-key`,
    JSON.stringify({
      url: `https://example.com/test-${Math.random()
        .toString(36)
        .substring(2, 9)}`,
    }),
    params
  );

  // Customize these checks based on your API's expected behavior
  check(response1, {
    "POST /short-key status is 200": (r) => r.status === 200,
    "POST /short-key response time < 500ms": (r) => r.timings.duration < 500,
    "POST /short-key has short_key": (r) => {
      try {
        return JSON.parse(r.body).hasOwnProperty("short_key");
      } catch {
        return false;
      }
    },
    "POST /short-key has original_url": (r) => {
      try {
        return JSON.parse(r.body).hasOwnProperty("original_url");
      } catch {
        return false;
      }
    },
  }) || errorRate.add(1);

  // Test POST /short-key/custom

  let response2 = http.post(
    `${BASE_URL}/short-key/custom`,
    JSON.stringify({
      url: `https://google.com/page-${Math.random()
        .toString(36)
        .substring(2, 8)}`,
      custom_key: `custom-${Math.random().toString(36).substring(2, 8)}`,
    }),
    params
  );

  // Customize these checks based on your API's expected behavior
  check(response2, {
    "POST /short-key/custom status is 200": (r) => r.status === 200,
    "POST /short-key/custom response time < 500ms": (r) =>
      r.timings.duration < 500,
    "POST /short-key/custom has short_key": (r) => {
      try {
        return JSON.parse(r.body).hasOwnProperty("short_key");
      } catch {
        return false;
      }
    },
    "POST /short-key/custom has original_url": (r) => {
      try {
        return JSON.parse(r.body).hasOwnProperty("original_url");
      } catch {
        return false;
      }
    },
  }) || errorRate.add(1);

  // Extract short_key from first response for GET test
  let shortKey = "test-key";
  try {
    if (response1.status === 200) {
      const data = JSON.parse(response1.body);
      shortKey = data.short_key || "test-key";
    }
  } catch (e) {
    // Use default key if parsing fails
  }

  let response3 = http.get(`${BASE_URL}/short-key/${shortKey}`, params);

  check(response3, {
    "GET /short-key/{short-key} status is 200 or 302": (r) =>
      r.status === 200 || r.status === 302,
    "GET /short-key/{short-key} response time < 500ms": (r) =>
      r.timings.duration < 500,
  }) || errorRate.add(1);

  sleep(0.1);
}
