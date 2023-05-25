# QuestionGen

QuestionGen is a web application that leverages Glyphic's question generation model to generate questions based on user-provided articles or texts. The application utilizes a model inference service hosted on an AWS serverless Lambda function, which is exposed through an API Gateway. The frontend, built using Vue.js, interacts with the API endpoint to enable users to generate questions for their input texts.

## Backend

The backend of QuestionGen comprises a Lambda function which is written in Python and containerized, allowing for easy deployment, local development, and testing. The provisioning of the backend was accomplished using AWS SAM (Serverless Application Model) and CloudFormation. This architecture ensures scalability and flexibility for the application.

## Frontend

QuestionGen's frontend is developed using Vue.js and is hosted on AWS Amplify. Users can input articles of up to 2500 characters, and the application generates relevant questions based on the provided text. The frontend interacts with the API endpoint exposed by the backend to facilitate question generation.

### Features

QuestionGen offers the following features:

- **Article Input:** Users can enter articles or texts of up to 2500 characters to generate questions.
- **Question Generation Modes:** The application supports two modes of question generation:
  - **Batch Mode:** Multiple questions are generated without any specific target answer.
  - **Target Answer Mode:** Users can provide a target answer, and the application generates a question based on the provided answer.
  Users can easily switch between these modes using the mode toggle button available on the toolbar.
- **Multiple Conversations:** Users can maintain multiple conversations within the application. They can start new conversations using the dedicated button on the toolbar and utilize the navigation and delete buttons to manage their conversations effectively.
- **Export to JSON:** The application includes an export feature that allows users to save their question generations as a JSON file. Users can utilize the export to JSON button available on the toolbar to accomplish this.

## Limitations

Although QuestionGen is a functional web application, there are certain limitations due to the short development timeframe. The following are some of the limitations that would have been addressed given more time:

- **Session Management:** Currently, the application operates as a stateless service. If a user refreshes the page, their data will be lost. To address this, a distributed caching layer could have been implemented to manage user sessions effectively.
- **Provisioned Concurrency:** Lambda functions experience initial start-up latency, which can impact performance when the service has been idle for an extended period. By utilizing provisioned concurrency from AWS, the container would remain "warm" for longer durations, ensuring high-performance response times.

Please note that these limitations do not significantly impact the core functionality of the application, but their implementation would have enhanced user experience and performance.

I hope you enjoy using the app, it was a fun exercise for myself as well.