/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'deepankar', // the auth0 domain prefix
    audience: 'coffee', // the audience set for the auth0 app
    clientId: 'El3knBv0vV3cHz1IztfpNO6WZIuxdMic', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
