"use client";
import Footer from "@/components/Footer";
import Form from "@/components/Form";
import Header from "@/components/Header";
import React from "react";

import styles from "./page.module.css";
import {
  UrqlProvider,
  ssrExchange,
  cacheExchange,
  fetchExchange,
  createClient,
} from "@urql/next";

const Page = () => {
  return (
    <div className={styles.app}>
      <Header />
      <Form />
      <Footer />
    </div>
  );
};

export default () => {
  const [client, ssr] = React.useMemo(() => {
    const ssr = ssrExchange({
      isClient: typeof window !== "undefined",
    });
    const client = createClient({
      url: "http://127.0.0.1:3001/graphql",
      exchanges: [cacheExchange, ssr, fetchExchange],
      suspense: true,
    });

    return [client, ssr];
  }, []);
  return (
    <UrqlProvider client={client} ssr={ssr}>
      <Page />
    </UrqlProvider>
  );
};
