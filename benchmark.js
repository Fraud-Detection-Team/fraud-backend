import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 25,
  duration: '60s',
};

export default function () {
  const baseURL = 'https://fraud-backend-production.up.railway.app';

  // GET endpoints
  const getEndpoints = [
    '/payment_method/fraud/by-payment-method',
    '/Top5Merchant/fraud/by-mcc',
    '/TopUsers/spending/top-users',
    '/merchants/risk',
  ];

  for (let endpoint of getEndpoints) {
    let res = http.get(`${baseURL}${endpoint}`);
    check(res, {
      'status is 200': (r) => r.status === 200,
      'response time < 500ms': (r) => r.timings.duration < 500,
    });
  }

  // POST endpoint
  const payload = JSON.stringify({
    amount: 100.0,
    use_chip: "swipe transaction",
    mcc: 5411,
    errors: "None"
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  let res = http.post(`${baseURL}/fraud/predict`, payload, params);
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });

  sleep(1);
}
