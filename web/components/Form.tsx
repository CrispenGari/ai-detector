"use client";
import React from "react";
import styles from "./Form.module.css";
import { FaFileUpload } from "react-icons/fa";
import { FileUploader } from "react-drag-drop-files";
import { gql, useMutation } from "@urql/next";

const Form = () => {
  const [{ data, fetching, error }, detectAI] = useMutation(mutation);
  const [state, setState] = React.useState<{
    text: string;
    file: any;
    upload: boolean;
  }>({
    text: "",
    file: null,
    upload: false,
  });
  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!!state.file) {
      console.log({ file: state.file });
      await detectAI({ input: { text: null, file: state.file } });
    } else {
      await detectAI({ input: { text: state.text, file: null } });
    }
  };

  return (
    <>
      {state.upload ? (
        <div className={styles.file__modal}>
          <div className={styles.file__modal__form}>
            <h1>File Upload</h1>
            <FileUploader
              handleChange={(file: any) =>
                setState((s) => ({
                  ...s,
                  file,
                  upload: false,
                }))
              }
              name="file"
              types={["txt"]}
              className={styles.upload__form__dragzone}
              multiple={false}
            />
          </div>
        </div>
      ) : null}
      <div className={styles.form}>
        <form onSubmit={onSubmit}>
          {fetching ? (
            <div className={styles.loading}>
              <div className={styles.indicator} />
            </div>
          ) : null}
          {!!!state.file ? (
            <div className={styles.text_area}>
              <textarea
                value={state.text}
                onChange={(e) => {
                  setState((s) => ({ ...s, text: e.target.value }));
                }}
                placeholder="Paste a paragraph of less than 300 words..."
              ></textarea>
              <button type="submit">Detect</button>
            </div>
          ) : (
            <div className={styles.file_area}>
              <div className={styles.selected__file}>
                <p>{state.file?.name}</p>
                <button onClick={() => setState((s) => ({ ...s, file: null }))}>
                  remove
                </button>
              </div>
              <button type="submit">Detect</button>
            </div>
          )}
          <div>
            <button
              type="button"
              onClick={() => {
                setState((s) => ({ ...s, upload: true }));
              }}
              className={styles.icon__button}
            >
              <FaFileUpload />
            </button>
          </div>
        </form>

        {data?.predictAI?.prediction?.error ? (
          <div className={styles.error}>
            <h1>Error - {data?.predictAI?.prediction?.error.field}</h1>
            <p>{data?.predictAI?.prediction?.error.message}</p>
          </div>
        ) : undefined}

        {data?.predictAI?.prediction?.prediction ? (
          <div
            className={styles.result}
            style={{
              backgroundColor:
                data?.predictAI?.prediction?.prediction.classId !== 1
                  ? "#219b9d"
                  : "#ff8000",
            }}
          >
            <h1
              style={{
                color: "white",
                marginBottom: 5,
              }}
            >
              {data?.predictAI?.prediction?.prediction.className.toUpperCase()}{" "}
              Generated:
              {data?.predictAI?.prediction?.prediction.probability * 100}%
            </h1>
            <p>{data?.predictAI?.prediction?.prediction.text}</p>
          </div>
        ) : null}
      </div>
    </>
  );
};

export default Form;

const mutation = gql`
  fragment ErrorFragment on Error {
    field
    message
  }

  fragment PredictionFragment on Prediction {
    classId
    probability
    text
    className
  }

  fragment PredictionResponseFragment on PredictionResponse {
    error {
      ...ErrorFragment
    }
    prediction {
      ...PredictionFragment
    }
  }

  mutation PredictAI($input: AIHumanInput!) {
    predictAI(input_: $input) {
      ok
      prediction {
        ...PredictionResponseFragment
      }
    }
  }
`;
