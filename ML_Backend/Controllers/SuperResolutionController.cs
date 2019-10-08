using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using ML_Backend.Python;

namespace ML_Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class SuperResolutionController : ControllerBase
    {

        // POST: api/SuperResolution
        [HttpPost]
        public SuperImage Post([FromBody] SuperImage image)
        {
            // Will do all the machine learning stuff 
            SuperImage UpscaledImage = Solutions.SuperResolution(image);

            // the result should be again a SuperImage object.
            return UpscaledImage;

        }

    }
}
