import React from "react";
import styles from "./Footer.module.css";
import Link from "next/link";

const Footer = () => {
  return (
    <div className={styles.footer}>
      <p>
        {" "}
        Copyright © {new Date().getFullYear()}{" "}
        <Link href={"https://github.com/CrispenGari/ai-detector"}>
          AI Text Detector
        </Link>
        . All rights reserved.
      </p>
    </div>
  );
};

export default Footer;
