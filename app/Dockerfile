FROM gcc:latest

COPY . /app

WORKDIR /app/

RUN g++ -o napp napp.cpp

CMD ["./napp"]
