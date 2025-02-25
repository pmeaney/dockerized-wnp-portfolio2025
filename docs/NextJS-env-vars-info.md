
# NextJS Env Vars Info

In Next.js, environment variables have special prefixing rules that determine how they're exposed:

NEXT_PUBLIC_ prefix: Variables with this prefix (like NEXT_PUBLIC_MAIN_SITE_BASE_URL) are exposed to the browser/client-side JavaScript. This means they're:

- Available in both server and client code
- Embedded in the JavaScript bundle sent to the browser
- Accessible via process.env.NEXT_PUBLIC_VARIABLE_NAME in any file


Regular variables (without the prefix): Variables like NODE_ENV, HOSTNAME, and PORT are:

- Only available on the server side
- Not exposed to the browser
- Not included in client-side bundles
- Only accessible in server-side code (API routes, getServerSideProps, etc.)