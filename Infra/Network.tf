

resource "aws_vpc" "vpc_a" {
   cidr_block = "10.0.0.0/16"   
}


resource "aws_subnet" "vpc_a_subnet_public" {
  vpc_id = aws_vpc.vpc_a.id
  cidr_block = "10.0.1.0/24"

}
resource "aws_internet_gateway" "vpc_a" {
    vpc_id = aws_vpc.vpc_a.id
  tags = {
    Name = "internetgateway"
  }
}

resource "aws_subnet" "vpc_a_subnet_private"{
  vpc_id = aws_vpc.vpc_a.id
  cidr_block = "10.0.2.0/24"
}

resource "aws_subnet" "vpc_a_subnet_private2"{
  vpc_id = aws_vpc.vpc_a.id
  cidr_block = "10.0.3.0/24"

  tags = {
    name = "private2"
  }
}


resource "aws_route_table" "route_private2" {
  vpc_id = aws_vpc.vpc_a.id

  tags = {
    Name = "private_route2"
  }
}




resource "aws_route_table" "route_public" {
  vpc_id = aws_vpc.vpc_a.id

  route {

    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.vpc_a.id
  }

  tags = {
    Name = "public_route"
  }
}



resource "aws_route_table" "route_private" {
  vpc_id = aws_vpc.vpc_a.id

  tags = {
    Name = "private_route"
  }
}


# attcahments for networking

resource "aws_route_table_association" "public" {
    subnet_id = aws_subnet.vpc_a_subnet_public.id
    route_table_id = aws_route_table.route_public.id
  
}

resource "aws_route_table_association" "private" {
    subnet_id = aws_subnet.vpc_a_subnet_private.id
    route_table_id = aws_route_table.route_private.id 
}

resource "aws_route_table_association" "private2" {
    subnet_id = aws_subnet.vpc_a_subnet_private2.id
    route_table_id = aws_route_table.route_private2.id 
}




