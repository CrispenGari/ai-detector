import React from "react";

import styles from "./page.module.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import NotFound from "@/components/NotFound";
const Page = () => {
  return (
    <div className={styles.app}>
      <Header />
      <NotFound />
      <Footer />
    </div>
  );
};

export default Page;
