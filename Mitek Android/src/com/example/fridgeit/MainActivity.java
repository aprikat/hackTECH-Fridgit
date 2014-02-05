package com.example.fridgeit;

import java.io.*;
import java.net.URL;
import java.security.SecureRandom;
import java.util.HashMap;

import javax.net.ssl.*;

import org.json.JSONException;
import org.json.JSONObject;

import com.miteksystems.android.mobileimaging.library.MIUser;
import com.miteksystems.android.mobileimaging.library.Transaction;
import com.miteksystems.android.mobileimaging.library.results.InsertPhoneTransactionResult;
import com.miteksystems.android.mobileimaging.library.results.MitekCaptureJobSettingsResult;
import com.miteksystems.misnap.MiSnap;
import com.miteksystems.misnap.MiSnapAPI;

import android.os.Bundle;
import android.provider.Settings;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.util.Base64;
import android.util.Log;
import android.view.Menu;
import android.widget.Toast;

public class MainActivity extends Activity {

	public static final int RESULT_PICTURE_CODE = android.app.Activity.RESULT_FIRST_USER + 2;
	public boolean offlineMode = false;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		JSONObject jjs = null;
		try {
			jjs = new JSONObject();

			jjs.put(MiSnapAPI.Name, "Crop_IQA_OCR");
			jjs.put(MiSnapAPI.AllowVideoFrames, "1");
			jjs.put(MiSnapAPI.CameraDegreesThreshold,  "150");
		} catch (JSONException e) {
			e.printStackTrace();
		}                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
		Intent i = new Intent(MainActivity.this, MiSnap.class);
		i.putExtra(MiSnapAPI.JOB_SETTINGS, jjs.toString()); 
		startActivityForResult(i, MiSnapAPI.RESULT_PICTURE_CODE);


	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}


	/**
	* Callback from MiSnap
	* @see android.app.Activity#onActivityResult(int, int, android.content.Intent)
	*/


	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		
		
				if (MiSnapAPI.RESULT_PICTURE_CODE == requestCode) {
					String msg = "Sending for data extraction. Please wait...";
					if (null == data) {
						Log.e("HomeActivity", "null data!");
						return;
					}
					Bundle extras = data.getExtras();
					String miSnapResultCode = extras.getString(MiSnapAPI.RESULT_CODE);
					HashMap<String,String> mSettings;
					String SETTINGS_PREF = "settings";
					if (RESULT_OK == resultCode) {
						if (MiSnapAPI.RESULT_SUCCESS_VIDEO.equals(miSnapResultCode)
								|| MiSnapAPI.RESULT_SUCCESS_STILL.equals(miSnapResultCode)) {
							// pull image
							byte[] mRawImage = data.getByteArrayExtra(MiSnapAPI.RESULT_PICTURE_DATA);
							byte[] mEncodedImage = Base64.encode(mRawImage, Base64.DEFAULT);
							
							Serializable settings = getIntent().getSerializableExtra(SETTINGS_PREF);
							if (null != settings) {
								// don't know WHY it won't cast straight to object
								mSettings = (HashMap<String, String>) settings;
								//live with the warning -> http://stackoverflow.com/a/2890491/774691
							}
							

							MitekContext.ResultMetrics
							= data.getStringExtra(MiSnapAPI.RESULT_METRICS);
							String server = "https://mip03.ddc.mitekmobile.com/MobileImagingPlatformWebServices/ImagingPhoneService.asmx";
							String user = "tcparker@hack.com";
							String password = "Tcparker123!";
							String org = "MitekHack";
							
							
							MitekContext.Library = new MIUser(server, user, password, org, Settings.Secure.ANDROID_ID);
							// process login - AsyncTransactionReturn will be called when the server
							// is done
								MitekContext.mMitekJobSettingsResult = new MitekCaptureJobSettingsResult();
								MitekContext.mMitekJobSettingsResult.mJobSettings.put(MiSnapAPI.JOB_SETTINGS, "DRIVERS_LICENSE_CA");
							                   
							new Transaction(this, 
									MitekContext.Library,
									MitekContext.mMitekJobSettingsResult, 
									mEncodedImage, 
									msg);
						}
					} else if (RESULT_CANCELED == resultCode) {
						if (MiSnapAPI.RESULT_CAMERA_NOT_SUFFICIENT.equals(miSnapResultCode)) {
							Toast.makeText(this, "Camera not operable or insufficient", Toast.LENGTH_LONG).show();
						} else {
							Toast.makeText(this, "MiSnap Canceled", Toast.LENGTH_SHORT).show();
						}
					}
				}

			
		
	}
	
	
	/*
	* Callback from Transaction
	* @see com.miteksystems.android.mobileimaging.library.AsyncTransaction#AsyncTransactionReturn(com.miteksystems.android.mobileimaging.library.results.InsertPhoneTransactionResult)
	*/
	//@Override
	public void AsyncTransactionReturn(InsertPhoneTransactionResult result) {
	MitekContext.InsertPhoneTransactionResult = result;


	if (-5 == result.SecurityResult) {
	// Show a dialog
	AlertDialog.Builder dialog = new AlertDialog.Builder(MainActivity.this);
	dialog.setTitle("Connection lost");
	dialog.setMessage("Going back to login screen");
	dialog.setPositiveButton("OK",
	new DialogInterface.OnClickListener() {
	public void onClick(DialogInterface dialog, int id) {
	dialog.cancel();
	startActivity(new Intent(MainActivity.this, LoginActivity.class)); // unsuccessful
	}
	});
	dialog.show();
	} else if (null != result.TransactionError) {
	// Show a dialog
	AlertDialog.Builder dialog = new AlertDialog.Builder(MainActivity.this);
	dialog.setTitle("Server error:");
	dialog.setMessage(result.IQAMessage);
	dialog.setPositiveButton("OK",
	new DialogInterface.OnClickListener() {
	public void onClick(DialogInterface dialog, int id) {
	dialog.cancel();
	}
	});
	dialog.show();
	} else { // successful
	Intent i = new Intent(MainActivity.this, ViewResultActivity.class);
	//i.putExtra("JOBNAME", shortDescription);
	startActivity(i);
	}
	}

	/*
	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
		setContentView(R.layout.end);

		if (requestCode == RESULT_PICTURE_CODE
				&& resultCode == Activity.RESULT_OK && data != null) {

			String miSnapResultCode = data.getStringExtra(MiSnapAPI.RESULT_CODE);
			if (MiSnapAPI.RESULT_SUCCESS_VIDEO.equals(miSnapResultCode)
					|| MiSnapAPI.RESULT_SUCCESS_STILL.equals(miSnapResultCode)) {

				byte[] mRawImage = data.getByteArrayExtra(MiSnapAPI.RESULT_PICTURE_DATA);
				byte[] mEncodedImage = Base64.encode(mRawImage, Base64.DEFAULT);	

				BufferedReader inputStream = null;
				try {
					File file = new File("C:\\Users\\User\\workspace\\FridgeIt\\bin\\res\\SOAPRequest.xml");
					inputStream = new BufferedReader(new InputStreamReader(getAssets().open("SOAPRequest.xml")));
					String currentLine = "";
					StringBuilder request = new StringBuilder();
					while ((currentLine = inputStream.readLine()) != null) {
						if(currentLine.contains("_IMG_")) {
							currentLine = currentLine.replace("_IMG_", new String(mEncodedImage));
						}
						request.append(currentLine);
					}

					String requestString = request.toString();
					String url = "https://mip03.ddc.mitekmobile.com/MobileImagingPlatformWebServices/ImagingPhoneService.asmx";

					String results = postDocument(url, request.toString());



				} catch (FileNotFoundException e) {
					e.printStackTrace();
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}


			}
		} else if (requestCode == RESULT_PICTURE_CODE
				&& resultCode == Activity.RESULT_OK && data == null) {
			// user cancelled the action or hit the back button
		} else if (resultCode == Activity.RESULT_CANCELED){
			// an error occurred in the Capture Library
		}

	}

	 */

	private String postDocument(String svcUrl,String data) throws Exception {
		URL url = null;
		HttpsURLConnection con = null;
		InputStream inputStream = null;
		OutputStream outputStream = null;
		InputStream errorInputStream = null;
		int responseCode= -1;
		ByteArrayOutputStream baos = new ByteArrayOutputStream(512);
		ByteArrayInputStream bais = null;

		if (Thread.interrupted())
			throw new InterruptedException();


		byte [] body = data.getBytes();
		url = new URL(svcUrl);	

		HttpsURLConnection.setDefaultHostnameVerifier(new NullHostNameVerifier());
		SSLContext context = SSLContext.getInstance("TLS");
		context.init(null, new X509TrustManager[]{ xCert()}, new SecureRandom());
		HttpsURLConnection.setDefaultSSLSocketFactory(context.getSocketFactory());

		con = (HttpsURLConnection) url.openConnection();
		con.setReadTimeout(60000);
		con.setConnectTimeout(15000);
		con.setDoInput(true);
		con.setDoOutput(true); 
		con.setUseCaches(false);  			
		con.setRequestMethod("POST");
		con.setRequestProperty("Content-Type", "text/xml; charset=UTF-8");

		con.setRequestProperty("Content-Length", Integer.toString(body.length));


		if (Thread.interrupted())
			throw new InterruptedException();


		outputStream = con.getOutputStream(); 
		outputStream.write(body);
		outputStream.flush();


		responseCode = con.getResponseCode();


		if (Thread.interrupted())
			throw new InterruptedException();


		if (HttpsURLConnection.HTTP_OK == responseCode) {
			inputStream = con.getInputStream();				
			byte buf[] = new byte[2048];				
			int n;

			while ((n = inputStream.read(buf)) != -1) {			
				baos.write(buf, 0 ,n);
			}

			bais = new ByteArrayInputStream( baos.toByteArray() );
		} else {
			//Read error stream -- Not doing this may give responseCode of -1 with the HTTPUrlConnection object	
			errorInputStream = con.getErrorStream();


			if (null != errorInputStream) {
				int i;
				while (-1 != (i = errorInputStream.read())){
					baos.write(i);
				}
			}

			bais = new ByteArrayInputStream( baos.toByteArray() );
		}

		//FOR TESTING ONLY -
		//uncomment below lines to eval returned Soap. However, will error on results page.
		Reader r = new InputStreamReader(bais);
		StringWriter sw = new StringWriter();
		char[] buffer = new char[1024];
		for(int n; (n=r.read(buffer)) !=1;)
			sw.write(buffer, 0, n);
		Log.v("MiSnap", ""+sw.toString());
		return sw.toString();

		//return new InputStreamReader(bais);
	}

	private static X509TrustManager xCert() {
		return new X509TrustManager() {


			public java.security.cert.X509Certificate[] getAcceptedIssuers() {
				return null;
			}


			public void checkClientTrusted(java.security.cert.X509Certificate[] chain, 
					String authType) {
			}


			public void checkServerTrusted(java.security.cert.X509Certificate[] chain, 
					String authType) {
				// if we want to check the server cert, do it here...
			}
		};
	}

	final static HostnameVerifier DO_NOT_VERIFY = new HostnameVerifier() {
		public boolean verify(String hostname, SSLSession session) {
			return true;
		}
	};

	public class NullHostNameVerifier implements HostnameVerifier {


		public boolean verify(String hostname, SSLSession session) {	        
			return true;
		}
	}



}
