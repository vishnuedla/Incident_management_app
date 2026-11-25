resource "aws_key_pair" "terraform_key" {
  key_name   = "vishnu"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQCbyQHUCZtFyVEf2/YilXM0Mh+Cn5yKoNcGTVXeUhcA/wBSTkT+Efs7kuMRnamNhEtV/zPLQFklfwz+b1v6wMn1sP1RZLoIz5QACs/3dHgwAavsl8QmKXT+5fTWpVyY/9IdDm8OQm5WfDMsVfU3NhfdfVp2kLGoPkNJ9fXqLRiK8uZ4J77AjoL2DePaxrQDeP0Halnd1v/jmkxmKESU/vQIpbj3euykkHL9TLNkLS0iHfMPxQojmV97p8vIIK2Jga9i245jYJqK+qVx6O9CuSFadLta08+Ot8X+BArGw4sCaDUKq4FqvkaLz0/SXcehgBTytbjuvE/x6rhHZDASK/azPH4aq7jRnGmUJPerGC7xYnRzi2l3Mp965zPcClM9pM7Fq64/ROMxHV7+iO+QBr35putgk3oj0Q8HjYmuvW5lrOOvR1zUcD5vbRTezf0aczpCj2hktV/JMHeWyRtCQ/87HCXff9u0Ap0PXFy9U2DlI0u4iktpCFcEVF4dJy9FnoGiUplyPQZw33ILenMoZQCbJHF7D8e5CKIarkylUNEDyEDfZCcambhxiL9sjxbh8XDPVahS2/dMlkQksQ/pS5Oq/WopC/FXIrprBnEz/w2sJb8OMMN8AlVaiGpnNTelxPV7PaIRVgeZgT2nbrodLl4U76Qtyp3eXK5Dd5JGIczHlw== vishnu@Vishnu"
}

resource "aws_instance" "jump_server" {
    ami = "ami-02f853b31ccb5871f" 
    instance_type = "t3.micro"
    key_name = aws_key_pair.terraform_key.key_name
    subnet_id = aws_subnet.vpc_a_subnet_public.id 
}


resource "aws_security_group" "jump_server_sg" {
  name        = "jump_server_sg"
  description = "Security group for jump server"
  vpc_id      = aws_vpc.vpc_a.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]

  }
  


