import React from "react";
import styles from "./Header.module.css";
import Image from "next/image";
import { FaGithub } from "react-icons/fa";
import Link from "next/link";

const Header = () => {
  return (
    <div className={styles.header}>
      <Link href={"/"}>
        <Image alt="logo" src={"/logo.png"} width={30} height={30} />
        <h1>AI Text Detector</h1>
      </Link>

      <Link href={"https://github.com/CrispenGari/ai-detector"}>
        <FaGithub className={styles.header__icon} />
      </Link>
    </div>
  );
};

export default Header;
