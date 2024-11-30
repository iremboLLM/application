// app/api/agent/route.js

import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    // Extract the request body
    const requestBody = await req.json();

    const response = await fetch("http://localhost:8000/agent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody), // Forward the request body
    });

    // Check if the response is OK (status 200)
    if (!response.ok) {
      return NextResponse.json(
        { error: "Failed to fetch data from localhost:8000/agent" },
        { status: response.status }
      );
    }

    // Parse the response from the API
    const data = await response.json();

    // Return the response data
    return NextResponse.json(data, { status: 200 });
  } catch (error: unknown) {
    console.error(error);
    return NextResponse.json(
      {
        error:
          "An error occurred while fetching data from localhost:8000/agent",
      },
      { status: 500 }
    );
  }
}
