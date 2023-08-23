from Website import create_app

app=create_app()



if __name__=="__main__":
    app.run(host="192.168.111.226",port=5200,debug=True)
