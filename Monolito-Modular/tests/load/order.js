import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 50,
  iterations: 500,
};

export default function () {
  const payload = JSON.stringify({
    order_items: [
      {
        quantity: 1,
        item_id: 1,
      },
    ],
  });

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  const response = http.post(
    "http://localhost:8000/orders/",
    payload,
    params
  );

  console.log("STATUS:", response.status);
  console.log("BODY:", response.body);

  check(response, {
    "status 200 ou 201": (r) =>
      r.status === 200 || r.status === 201,
  });
}