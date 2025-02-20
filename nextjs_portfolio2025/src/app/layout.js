import "./portfolio/scss/bulma-import.scss";
import Head from "next/head";

export const metadata = {
  title: "Patrick's Portfolio",
  description: "Welcome to Patrick's Portfolio",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <Head>
        <link
          rel="stylesheet"
          href="https://use.fontawesome.com/releases/v5.4.1/css/all.css"
        />
        <link
          href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,700"
          rel="stylesheet"
        />
      </Head>
      <body>{children}</body>
    </html>
  );
}
