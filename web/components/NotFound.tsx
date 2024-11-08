import React from "react";

import styles from "./NotFound.module.css";
import Link from "next/link";
const NotFound = () => {
  return (
    <div className={styles.not__found}>
      <h1>Ops! Page not Found</h1>
      <h2>
        <span>4</span>
        <span>0</span>
        <span>4</span>
      </h2>
      <Link href={"/"}>Go to Home</Link>
    </div>
  );
};

export default NotFound;
