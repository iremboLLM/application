import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  webpack: (config, { isServer }) => {
    if (isServer) {
      // Disable Turbopack for the server-side
      config.resolve.alias["react-server-dom-turbopack/server.edge"] =
        "react-server-dom-webpack/server.edge";
    }
    return config;
  },
  experimental: {
    // turbopack: false, // Disable turbopack
  },
};

export default nextConfig;
